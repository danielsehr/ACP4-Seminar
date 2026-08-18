import pandas as pd
import matplotlib.pyplot as plt

from dataclasses import fields
from ACP4.processing.read_data import Data


def align_timeseries(
    data: Data,
    ) -> Data:
    
    start = max(
        getattr(data, field.name).index.min()
        for field in fields(data)
    )
    
    end = min(
        getattr(data, field.name).index.max()
        for field in fields(data)
    )
    
    for field in fields(data):
        df = getattr(data, field.name)
        setattr(df, field.name, df.loc[start:end])


def print_data_length(data: Data) -> None:
    
    for field in fields(data):
        df = getattr(data, field.name)
        
        print(f"Name: {field.name}")
        print("Length of available data:")
        print(f"{df.index.max() - df.index.min()}")
        print("------------------------")


def check_missing_values(data: Data) -> None:
    
    for field in fields(data):
        df = getattr(data, field.name)

        na_count = df.isna().sum()
        na_count = na_count[na_count > 0]

        print(f"Name: {field.name}")

        if na_count.empty:
            print("No missing values.")
        else:
            print(f"Number of NAs:\n{na_count}")
            print(f"Percentage of NAs:\n{(na_count / len(df) * 100).round(2)}%")

        print("------------------------")
        
        
def plot_daily_flow(df: pd.Series) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        df.index,
        df["discharge_spec_obs"],
        linewidth=1.0,
    )

    ax.set_title("Watershed: DEB10810, Klingbach, Herxheim")
    ax.set_xlabel("Date")
    ax.set_ylabel("Observed catchment-specific discharge [mm/d-1]")

    # ax.xaxis.set_major_locator(mdates.YearLocator())
    # ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.grid(
        True,
        alpha=0.3,
        linewidth=0.8,
    )

    fig.tight_layout()

    plt.show()