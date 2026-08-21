import pandas as pd
from dataclasses import fields
from acp4.io.read_data import Data


agro_column_mapping = {
    "SUM_NN050": "precipitation_mean",
    "AVG_RH200": "humidity_mean",
    "SUM_GS200": "radiation_global_mean",
    "AVG_TA200": "temperature_mean",
    "MIN_TA200min": "temperature_min",
    "MAX_TA200max": "temperature_max",
    "SUM_PEN": "potential_evapotranspiration",
}


def rename_agro_data(
    data: dict, 
    mapping: dict = agro_column_mapping
    ) -> dict:
    
    for key, df in data.items():
        df = df.rename(columns=mapping)
        
        data[key] = df

    return data


def intersect_columns(data: Data) -> Data:

    common_columns = None

    for field in fields(data):
        df = getattr(data, field.name)
        
        if field.name == "discharge":
            continue
        
        if common_columns is None:
            common_columns = df.columns
        else:
            common_columns = common_columns.intersection(df.columns)

    for field in fields(data):
        df = getattr(data, field.name)
        
        if field.name == "discharge":
            continue
        
        setattr(
            data,
            field.name,
            df.loc[:, common_columns]
        )

    return data
    

def intersect_datetime(data: Data) -> Data:
    
        start = max(
            getattr(data, field.name).index.min()
            for field in fields(data)
        )
        
        end = min(
            getattr(data, field.name).index.max()
            for field in fields(data)
        )
        
        return Data(
            **{
                field.name: getattr(data, field.name).loc[start:end]
                for field in fields(data)
            }
        )


def align_climate_timeseries(data: Data) -> Data:
    
    data = intersect_columns(data=data)
    data = intersect_datetime(data=data)
    
    return data


def mean_by_month(df: pd.DataFrame) -> pd.DataFrame:
    df = (
        df[["temperature_mean", "humidity_mean", "radiation_global_mean"]]
        .groupby(df.index.month)
        .agg(["mean", "std"])
        .round(2)
    )
    
    df.index = pd.to_datetime(df.index, format="%m").strftime("%b")
    
    return df