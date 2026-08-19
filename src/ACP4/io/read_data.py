from pathlib import Path
import pandas as pd
from dataclasses import dataclass, fields


@dataclass
class Data:
    discharge: pd.DataFrame
    camel: pd.DataFrame
    agro_herxheimweyher: pd.DataFrame
    agro_steinweiler: pd.DataFrame


def filter_camel_for_gauge_id(
    timeseries_dir: str | Path,
    gauge_id: str
    ):
    
    return [
        p 
        for p in Path(timeseries_dir).rglob("*.csv") 
        if gauge_id in p.stem.split("_")[4]
    ][0]


def read_camel_data(
    timeseries_dir: str | Path,
    gauge_id: str
    ) -> pd.DataFrame:
    
    filepath = filter_camel_for_gauge_id(
        timeseries_dir=timeseries_dir,
        gauge_id=gauge_id
        )
    
    df = pd.read_csv(
        filepath_or_buffer=filepath, 
        sep=",", decimal="."
        )

    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    
    return df


def read_agro_data(timeseries_dir: str) -> dict:
    csv_paths = [p for p in Path(timeseries_dir).rglob("*.csv") if "concat" in str(p)]

    agro_dict = {}

    for path in csv_paths:
        file_name = path.stem
        df = pd.read_csv(filepath_or_buffer=path, sep=";")
        
        df = df.rename(columns={"Tag": "Date"})
        
        df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y")
        df = df.set_index("Date")
        
        agro_dict[file_name] = df
    
    return agro_dict