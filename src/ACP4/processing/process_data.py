import pandas as pd
from dataclasses import fields
from typing import NamedTuple
import pymannkendall as mk

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

class TrendMetrics(NamedTuple):
    mk_orig: object
    # mk_hamed_rao: object
    sens_slope: object | None
    # seasonal_sens_slope: object | None


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


def agg_sum_mean_std(
    df: pd.DataFrame,
    cols: list[str],
    group_by: str
    ) -> pd.DataFrame:
    
    if group_by == "month":
        groups = df.index.month

    elif group_by == "year":
        groups = df.index.year
    
    return (
            df[cols]
            .groupby(groups)
            .agg(["sum", "mean", "std"])
            .round(2)
        )   


def summarize_data(
    df: pd.DataFrame,
    group_by: str
    ) -> pd.DataFrame:
    
    columns = ["temperature_mean", "humidity_mean", "radiation_global_mean", "discharge_spec_obs", "precipitation_mean"]

    available_columns = df.columns.intersection(columns).to_list()
    
    df = agg_sum_mean_std(
        df=df, 
        cols=available_columns, 
        group_by=group_by
    )

    if group_by == "month":
        df.index = pd.to_datetime(df.index, format="%m").strftime("%b")
        
    return df


# --- 4. Rainfall Analysis --- #
def agg_annually_sum(df: pd.DataFrame | pd.Series) -> pd.DataFrame | pd.Series:
    
    months_per_year = (
        df
        .groupby(df.index.year)
        .apply(lambda x: x.index.month.nunique())
    )
    
    complete_years = months_per_year[months_per_year == 12].index
    
    df = df[df.index.year.isin(complete_years)]
    
    return(
        (df
         .groupby([df.index.year])
         .agg(["sum", "std"])
         .round(2)
        )
    )


def agg_all_annually_sum(data: Data) -> dict:
    result = {}
    
    for field in fields(data):
        if field.name == "discharge":
            continue
        
        df = getattr(data, field.name)
        
        df_aggregated = agg_annually_sum(df=df["precipitation_mean"])

        result[field.name] = df_aggregated
    
    return(result)
    

def agg_monthly_precip_sum(df: pd.DataFrame) -> pd.DataFrame:
    
    df = (
        df
        .groupby(df.index.to_period("M"))
        .sum()
        .rename("precipitation")
        .to_frame()
    )

    df["month"] = df.index.month
    
    return(df)


def agg_all_monthly_precip_sum(data: Data) -> dict:
    result = {}
        
    for field in fields(data):
        if field.name == "discharge":
            continue
        
        df = getattr(data, field.name)
        
        df_aggregated = agg_monthly_precip_sum(df=df["precipitation_mean"])
        
        result[field.name] = df_aggregated
            
    return(result)        



# --- 5. Streamflow Analysis --- #
def agg_annually_discharge(
    df: pd.Series,
    complete_years_only: bool = True,
    ) -> pd.DataFrame | pd.Series:
    
    if complete_years_only:
        months_per_year = (
            df
            .groupby(df.index.year)
            .apply(lambda x: x.index.month.nunique())
        )
        
        complete_years = months_per_year[months_per_year == 12].index
        
        df = df[df.index.year.isin(complete_years)]
    
    return(
        (df
         .groupby([df.index.year])
         .agg(["mean", "sum", "max", "std", "count"])
         .round(2)
        )
    )
    
    
def agg_monthly_discharge_mean(df: pd.Series) -> pd.DataFrame:
    
    df = (
        df
        .groupby(df.index.to_period("M"))
        .sum()
        .rename("spec_discharge")
        .to_frame()
    )

    df["month"] = df.index.month
    df["year"] = df.index.year
    
    return(df)    


def subset_high_low_values(df: pd.Series) -> dict[str, pd.Series]:
    p95 = df.quantile(0.95)
    p05 = df.quantile(0.05)

    # print(f"p05: {p05:.2f}")
    # print(f"p95: {p95:.2f}")
    
    return(
        {
            "Q05": df[df < p05],
            "Q95": df[df > p95],
        }
    )


def calc_trend_metrics(df: pd.Series) -> TrendMetrics:

    # Mann-Kendall-Test
    mk_orig_results = mk.original_test(x_old=df, alpha=0.05)
    mk_hamed_rao_results = mk.hamed_rao_modification_test(x_old=df, alpha=0.05)


    # Theil-Sen's Slope Estimator
    if mk_orig_results.h and mk_hamed_rao_results.h:
        sens_slope = mk.sens_slope(df)

        # Needs to_numpy due to bug in source code. -> Need to open an issue or PR
        seasonal_sens_slope = mk.seasonal_sens_slope(df.to_numpy())
    
    else:
        sens_slope = None
        seasonal_sens_slope = None
    
    return(
        TrendMetrics(
            mk_orig=mk_orig_results,
            # mk_hamed_rao=mk_hamed_rao_results,
            sens_slope=sens_slope,
            # seasonal_sens_slope=seasonal_sens_slope
        )
    )
    
