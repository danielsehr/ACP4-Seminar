import numpy as np
import pandas as pd
from dataclasses import fields

import calendar
import statsmodels.formula.api as smf

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import matplotlib.dates as mdates
import seaborn as sns

from acp4.io.read_data import Data
from acp4.processing.process_data import summarize_data


mapping = {
    "camel": "Camel",
    "agro_herxheimweyher": "Herxheimweyher (Agrometeo)",
    "agro_steinweiler": "Steinweiler (Agrometeo)",
}


# --- 3. Climate Analysis --- #
def print_minmax_month(data: Data) -> None:
    for field in fields(data):
        df = getattr(data, field.name)
        
        if "discharge" in field.name:
            continue
        
        df = summarize_data(df=df, group_by="month")
        
        print(field.name)

        print("Coldest months:")
        print(df["temperature_mean"]["mean"].idxmin())
        
        print("\nHottest months:")
        print(df["temperature_mean"]["mean"].idxmax())
        
        print("---------------------\n")
            
            
def add_pointplot(
    df: pd.DataFrame,
    column_name: str,
    ax: plt.Axes,
    color: str
    ) -> None:
    
    sns.pointplot(
        data=df,
        x=df.index,
        y=df[column_name]["mean"],
        errorbar=None,
        ax=ax,
        color=color
    )

    
def add_errorbar(
    df: pd.DataFrame, 
    column_name: str,
    ax: Axes
    ) -> None:

    ax.errorbar(
        x=range(len(df)),
        y=df[column_name]["mean"],
        yerr=df[column_name]["std"],
        fmt="none",
        capsize=4,
        color="black"
    )


def plot_monthly_temp_hum_rad(
    df: pd.DataFrame,
    name: str,
    ax: Axes,
    ) -> None:

    # Temperature
    add_pointplot(df=df, column_name="temperature_mean", ax=ax, color="red")
    add_errorbar(df=df, column_name="temperature_mean", ax=ax,)

    # Humidity
    add_pointplot(df=df,column_name="humidity_mean",ax=ax,color="blue",)
    add_errorbar(df=df,column_name="humidity_mean",ax=ax,)

    ax.set_xlabel("Month")
    ax.set_ylabel("\nMean montly temperature [°C]  |  humidity [%]")
    ax.set_title(
        f"Station: {name}"
    )

    # Radiation
    ax2 = ax.twinx()

    add_pointplot(df=df,column_name="radiation_global_mean",ax=ax2,color="orange",)

    ax2.set_ylabel("Mean montly global radiation [W/m²]")


def plot_all_monthly_temp_hum_rad(data: Data) -> None:

    datasets = [
        (field.name, getattr(data, field.name))
        for field in fields(data)
        if "discharge" not in field.name
    ]

    n = len(datasets)

    fig, axes = plt.subplots(
        nrows=1,
        ncols=n,
        figsize=(6 * n, 5),
        squeeze=False,
    )

    axes = axes[0]

    for ax, (name, df) in zip(axes, datasets):

        df_monthly = summarize_data(df=df, group_by="month")

        plot_monthly_temp_hum_rad(
            df=df_monthly,
            name=name,
            ax=ax
        )

    fig.tight_layout()
    plt.show()
        

def plot_pet_comparison(
    camel_pet: pd.Series,
    hargreaves_pet: pd.Series,
    ax: Axes
    ) -> None:
    
    ax.scatter(
        camel_pet.index, 
        camel_pet.values, 
        s=1, 
    )
    
    ax.scatter(
        hargreaves_pet.index,
        hargreaves_pet.values,
        s=1,
    )
    
    ax.set_xlabel("Date")
    ax.set_ylabel("PET [mm d⁻¹]")
    ax.grid(alpha=0.3)
    
    
def plot_both_pet_comparison(
    camel_pet: pd.Series,
    herxheimweyher_pet: pd.Series,
    steinweiler_pet: pd.Series,
    ) -> None:
    
    agrometeo_pets = {
        "Herxheimweyher (Hargreaves)": herxheimweyher_pet,
        "Steinweiler (Hargreaves)": steinweiler_pet,
    }

    fig, axs = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(12, 5),
        sharey=True,
    )

    for ax, (name, pet) in zip(axs, agrometeo_pets.items()):

        ax.scatter(
            camel_pet.index,
            camel_pet.values,
            s=1,
            label="Camels",
        )

        ax.scatter(
            pet.index,
            pet.values,
            s=1,
            label=name,
        )

        ax.set_title("Comparison Camels PET and Hargreaves PET")
        ax.set_xlabel("Date")
        ax.set_ylabel("PET [mm d⁻¹]")
        ax.grid(alpha=0.3)
        ax.legend()

    fig.tight_layout()
    plt.show()


        
# --- 4. Rainfall Analysis --- #
def plot_annual_precip_sum(
    df: pd.DataFrame | pd.Series,
    ax: Axes,
    location: str
    ) -> None:

    mapping = {
        "camel": "Camel",
        "agro_herxheimweyher": "Herxheimweyher (Agrometeo)",
        "agro_steinweiler": "Steinweiler (Agrometeo)",
    }
    
    ax.bar(
        df.index,
        df["sum"],
        yerr=df["std"],
        capsize=3,
        alpha=0.8,
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Mean precipitation [mm]")
    ax.set_title(mapping[location])
    ax.grid(
        axis="y",
        alpha=0.3,
    )


def plot_all_annual_precip_sum(data: dict) -> None:
    
    fig, axs = plt.subplots(figsize=(9, 7), nrows=3)
    
    for ax, (key, df) in zip(axs, data.items()):
        plot_annual_precip_sum(df=df, ax=ax, location = key)
    
    plt.suptitle("Mean annually precipitation sum, period: 2015 - 2020")
    
    fig.tight_layout()
    plt.show()


def plot_monthly_precip_sum(
    df: pd.DataFrame | pd.Series,
    ax: Axes,
    location: str
    ) -> None:
    
    mapping = {
        "camel": "Camel",
        "agro_herxheimweyher": "Herxheimweyher (Agrometeo)",
        "agro_steinweiler": "Steinweiler (Agrometeo)",
    }

    df.boxplot(
        column="precipitation",
        by="month",
        ax=ax,
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Monthly precipitation [mm]")

    ax.set_xticklabels(
        [calendar.month_abbr[i] for i in range(1, 13)]
    )

    # Add jittered observations
    for month in range(1, 13):
        values = df.loc[
            df["month"] == month,
            "precipitation",
        ]

        x = np.random.normal(
            loc=month,
            scale=0.08,
            size=len(values),
        )

        ax.scatter(
            x,
            values,
            s=12,
            alpha=0.6,
        )

    ax.set_title(mapping[location])
    
    
def plot_all_monthly_precip_sum(data: dict) -> None:
    fig, axs = plt.subplots(figsize=(9, 7), nrows=3, sharey=True)
        
    for ax, (key, df) in zip(axs, data.items()):
        plot_monthly_precip_sum(df=df, ax=ax, location = key)
    
    plt.suptitle("Monthly precipitation sum, period: 2014 - 2020")
    
    fig.tight_layout()
    plt.show()
    

def plot_extreme_rainfall_events(
    df: pd.Series,
    ax: Axes,
    location: str
    ) -> None:
    
    p99 = df.quantile(0.99)

    colors = df.gt(p99).map({
        True: "red",
        False: "steelblue",
    })
    
    
    mapping = {
        "camel": "Camel",
        "agro_herxheimweyher": "Herxheimweyher (Agrometeo)",
        "agro_steinweiler": "Steinweiler (Agrometeo)",
    }

    ax.bar(
        df.index,
        df,
        color=colors,
    )

    ax.axhline(
        p99,
        linestyle="--",
        label=f"99th percentile = {p99:.2f}",
    )

    ax.set_title(mapping[location])
    ax.set_ylabel("Value")
    ax.legend()


def plot_all_extreme_rainfall_events(data: Data) -> None:
    
    fig, axs = plt.subplots(figsize=(12, 7), nrows=3, sharex=True)
    
    plot_fields = [
        field for field in fields(data)
        if field.name != "discharge"
    ]

    for ax, field in zip(axs, plot_fields):
        
        if field.name == "discharge":
            continue
        
        df = getattr(data, field.name)
        
        plot_extreme_rainfall_events(
            df=df["precipitation_mean"], 
            ax=ax, 
            location = field.name
        )
    
    fig.tight_layout()
    plt.show()
    


# --- 5. Streamflow Analysis --- #
def plot_annual_discharge_sum(
    df: pd.DataFrame | pd.Series,
    ) -> None:
    
    plt.bar(
        df.index,
        df["sum"],
        yerr=df["std"],
        capsize=3
    )
    plt.ylabel("Annual flow [m3/s]")
    plt.title("Mean annual specific discharge sums")
    plt.grid(
        axis="y",
        alpha=0.3,
    )


def plot_monthly_discharge_mean(
    df: pd.DataFrame | pd.Series,
    ) -> None:
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.boxplot(
        [
            df.loc[df["month"] == month, "spec_discharge"]
            for month in range(1, 13)
        ],
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Monthly specific discharge mean [mm]")
    
    ax.set_xticks(
        range(1, 13),
        [calendar.month_abbr[i] for i in range(1, 13)],
    )

    # Add jittered observations
    for month in range(1, 13):

        values = df.loc[
            df["month"] == month,
            "spec_discharge",
        ]

        x = np.random.normal(
            loc=month,
            scale=0.08,
            size=len(values),
        )

        ax.scatter(
            x,
            values,
            s=12,
            alpha=0.6,
        )

    ax.set_title(
        "Monthly specific discharge mean, period: 2014–2020"
    )

    fig.tight_layout()
    plt.show()


def plot_annual_max_flow_days(
    df: pd.Series,
    max_flows: pd.Series
    ) -> None:
    
    
    fig, ax = plt.subplots(figsize=(12, 7))

    max_flows_ts = df.loc[df.isin(max_flows)]

    ax.plot(
        df.index,
        df,
        color="steelblue",
    )

    ax.scatter(
        max_flows_ts.index,
        max_flows_ts,
        color="red",
        zorder=3,
    )


    ax.set_ylabel("Specific discharge [mm]")

    fig.tight_layout()
    plt.show()
    
    

def plot_rating_curve(df: pd.DataFrame) -> None:
    df["year"] = [p.year for p in df.index]

    fig, ax = plt.subplots()

    sc = ax.scatter(
        df["water_level_obs"],
        df["discharge_spec_obs"],
        c=df["year"],
        s=1
    )
    plt.colorbar(sc)

    ax.set_xlabel("[Observed daily water level [cm]")
    ax.set_ylabel("Observed volumetric discharge [m3 s-1]")

    plt.show()


def plot_discharge_trends(df: pd.Series) -> None:

    fig, axs = plt.subplots(
        nrows=3,
        sharex=True,
        figsize=(10, 8),
    )
    df = df.rename_axis("year").reset_index()

    variables = [
        ("mean", "Value [mm]", "Annual mean specific discharge"),
        ("max", "Value [mm]", "Annual maximum specific discharge"),
        ("sum", "Value [mm]", "Annual sum specific discharge"),
    ]

    for ax, (column, ylab, title) in zip(axs, variables):

        model = smf.ols(
            formula=f"{column} ~ year",
            data=df,
        )

        result = model.fit()
        trend = result.predict(df)

        ax.plot(
            df["year"],
            df[column],
            marker="o",
            label="Observed",
        )

        ax.plot(
            df["year"],
            trend,
            linestyle="--",
            label=(
                f"slope = {result.params['year']:.3f}\n"
                f"R² = {result.rsquared:.2f}"
            ),
        )

        ax.set_ylabel(ylab)
        ax.set_title(title)
        ax.legend()

    fig.tight_layout()
    plt.show()



def plot_high_low_percentile_flows(
    df: pd.Series,
    ) -> None:

    p95 = df.quantile(0.95)
    p05 = df.quantile(0.05)

    # Convert datetime index to Matplotlib's numeric date representation
    x = mdates.date2num(df.index)
    y = df.to_numpy()

    # Create line segments between consecutive observations
    points = np.column_stack([x, y])

    segments = np.stack(
        [points[:-1], points[1:]],
        axis=1,
    )

    # Color segments according to flow at their starting observation
    colors = np.where(
        y[:-1] > p95,
        "red",
        np.where(
            y[:-1] < p05,
            "blue",
            "grey",
        ),
    )

    fig, ax = plt.subplots(figsize=(12, 7))

    line = LineCollection(
        segments,
        colors=colors,
        linewidths=1,
    )

    ax.add_collection(line)

    # Format x-axis as dates
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m-%d")
    )

    # Legend proxies
    legend_lines = [
        Line2D(
            [0],
            [0],
            color="red",
            linewidth=2,
            label=f"> 95th percentile ({p95:.2f})",
        ),
        
        Line2D(
            [0],
            [0],
            color="blue",
            linewidth=2,
            label=f"< 5th percentile ({p05:.2f})",
        ),
    ]

    ax.legend(handles=legend_lines)

    ax.set_ylabel("Specific discharge [mm]")

    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()