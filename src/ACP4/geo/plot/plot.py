from pathlib import Path
import numpy as np
import geopandas as gpd
from rasterio.plot import plotting_extent

import matplotlib.pyplot as plt
import contextily as ctx

from acp4.io.read_data import read_landuse_csv


def plot_watershed_stations(
    points: gpd.GeoDataFrame,
    gauge: gpd.GeoDataFrame,
    watershed: gpd.GeoDataFrame,
    dem: np.ndarray,
    dem_transform,
    ) -> None:

    assert points.crs == watershed.crs
    
    fig, ax = plt.subplots(figsize=(10, 10))

    # DEM
    extent = plotting_extent(
        dem,
        transform=dem_transform,
    )
    
    im = ax.imshow(
        dem,
        extent=extent,
        cmap="terrain",
    )


    # Gauge station
    gauge.plot(
        ax=ax,
        color="blue",
        markersize=50,
    )
    for _, row in gauge.iterrows():
        ax.annotate(
            text="Gauge station",
            xy=(row.geometry.x, row.geometry.y),
            xytext=(-80, -8),
            textcoords="offset points",
        )
    

    # Weater stations
    points.plot(
        ax=ax,
        color="red",
        markersize=50,
    )

    for _, row in points.iterrows():
        ax.annotate(
            text=f"Weatherstation:\n{row['name']}",
            xy=(row.geometry.x, row.geometry.y),
            xytext=(-40, -35),
            textcoords="offset points",
        )

    # Watershed
    watershed.plot(
        ax=ax,
        facecolor="none",
        edgecolor="red",
        linewidth=1.5,
    )

    fig.colorbar(
        im,
        ax=ax,
        label="Elevation [m]",
    )

    
    ax.set_title("Watershed: DEB10810, Klingbach, Herxheim")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect("equal")

    fig.tight_layout()

    plt.show()
    

def plot_landuse(
    filepath: str | Path,
    ) -> None:
    
    df = read_landuse_csv(
        filepath=filepath,
    )

    df_plot = df.drop(columns=["gauge_id"]).loc[:, (df != 0).any(axis=0)]
    labels = df_plot.columns                                  

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.pie(
        df_plot.iloc[0],
        labels=labels, 
        autopct="%.1f%%",
        startangle=90
    )

    plt.tight_layout()
    plt.show()