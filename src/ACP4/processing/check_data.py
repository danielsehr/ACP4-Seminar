import pandas as pd
import matplotlib.pyplot as plt

from dataclasses import fields
from acp4.io.read_data import Data


def print_data_length(data: Data) -> None:
    
    for field in fields(data):
        df = getattr(data, field.name)
        
        print(f"Name: {field.name}")
        print(f"Length of available data: {df.index.max() - df.index.min()}")
        print(f"Period: {df.index.min()} - {df.index.max()}")
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
        

def check_duplicated_dates(data: Data) -> None:
    for field in fields(data):
        df = getattr(data, field.name)

        print(f"Name: {field.name}")
        print(f"Duplicated dates: {df.index.duplicated().any()}")
        print("------------------------")


def plot_flow_precip_temp(data: Data) -> None:
    fig, axs = plt.subplots(
    nrows=4,
    ncols=1,
    figsize=(12, 8),
    sharex=True,
    )

    # --- Discharge ---
    axs[0].plot(
        data.discharge.index,
        data.discharge["discharge_spec_obs"],
        linewidth=0.8,
        color="black"
    )

    axs[0].set_ylabel("Discharge [m³/s]")
    axs[0].grid(alpha=0.3)


    # --- Temperature and Precipitation ---
    plot_idx = 1

    for field in fields(data):
        if field.name == "discharge":
            continue

        df = getattr(data, field.name)

        ax_temp = axs[plot_idx]
        ax_precip = ax_temp.twinx()

        ax_temp.plot(
            df.index,
            df["temperature_mean"],
            linewidth=0.8,
            color="red",
        )

        ax_temp.set_ylabel("Temperature [°C]")

        ax_precip.bar(
            df.index,
            df["precipitation_mean"],
            width=1.0,
            alpha=0.5,
        )

        ax_precip.set_ylabel("Precipitation [mm]")
        ax_precip.invert_yaxis()

        ax_temp.set_xlabel("Date")
        ax_temp.grid(alpha=0.3)

        plot_idx += 1

    fig.tight_layout()

    plt.show()
        
        
def plot_flow_with_na(
    df: pd.DataFrame,
    start: str | None = None,
    end: str | None = None,
    ) -> None:
    
    if start is not None:
            df = df[df.index >= start]

    if end is not None:
        df = df[df.index < end]


    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        df.index,
        df["discharge_spec_obs"],
        linewidth=1.0,
    )
    
    # Missing observations
    na_mask = df["discharge_spec_obs"].isna()
    
    for date in df.index[na_mask]:
        ax.axvline(
            date,
            color="red",
            alpha=0.5,
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