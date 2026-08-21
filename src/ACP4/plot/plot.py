import pandas as pd
from dataclasses import fields
import matplotlib.pyplot as plt
import seaborn as sns

from acp4.io.read_data import Data
from acp4.processing.process_data import mean_by_month


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
    ax: plt.Axes
    ) -> None:

    ax.errorbar(
        x=range(len(df)),
        y=df[column_name]["mean"],
        yerr=df[column_name]["std"],
        fmt="none",
        capsize=4,
    )


def plot_monthly_temp(
    df: pd.DataFrame,
    name: str
    ) -> None:
    
    fig, ax = plt.subplots(figsize=(10, 6))

    add_pointplot(df=df, column_name="temperature_mean", ax=ax, color="red")    
    add_errorbar(df=df, column_name="temperature_mean", ax=ax)
    
    add_pointplot(df=df, column_name="humidity_mean", ax=ax, color="blue")    
    add_errorbar(df=df, column_name="humidity_mean", ax=ax)
        
    ax.set_xlabel("Month")
    ax.set_ylabel("Temperature [°C]  | Humidity [%]")
    ax.set_title(f"Mean monthly temperature ± standard deviation\nStation: {name}")
        
        
    ax2 = ax.twinx()        
    
    add_pointplot(df=df, column_name="radiation_global_mean", ax=ax2, color="orange")    
    # add_errorbar(df=df, column_name="radiation_global_mean", ax=ax2)
    ax2.set_ylabel("Global radiation [Wm²]")

    plt.tight_layout()
    plt.show()


def print_minmax_month(data: Data) -> None:
    
    for field in fields(data):
        df = getattr(data, field.name)
        
        if "discharge" in field.name:
            continue
        
        df = mean_by_month(df=df)
        
        print(field.name)

        print("Coldest months:")
        print(df["temperature_mean"]["mean"].idxmin())
        
        print("\nHottest months:")
        print(df["temperature_mean"]["mean"].idxmax())
        
        print("---------------------\n")


def plot_all_monthly_temp(data: Data) -> None:
    
    for field in fields(data):
        df = getattr(data, field.name)
        
        if "discharge" in field.name:
                    continue
        
        df = mean_by_month(df=df)
        
        plot_monthly_temp(df=df, name=field.name)
        

def plot_pet_comparison(
    camel_pet,
    hargreaves_pet
    ):
    
    fig, ax = plt.subplots()
    ax.scatter(camel_pet.index, camel_pet.values, s=0.1)
    ax.scatter(hargreaves_pet.index, hargreaves_pet.values, s=0.1)
    
    plt.show()