from pathlib import Path
import numpy as np
import geopandas as gpd
from rasterio.plot import plotting_extent

import matplotlib.pyplot as plt
from matplotlib import figure
import contextily as ctx

from acp4.io.read_data import read_landuse_csv


def plot_watershed_stations(
    points: gpd.GeoDataFrame,
    watershed: gpd.GeoDataFrame,
    ax: plt.Axes,
    ) -> None:
    
    points = points.to_crs("EPSG:3857")
    watershed = watershed.to_crs(crs="EPSG:3857")

    assert watershed.crs == points.crs

    points.plot(
        ax=ax,
        color="red",
        markersize=50,
    )

    for _, row in points.iterrows():
        ax.annotate(
            text=f"Station: {row['name']}",
            xy=(row.geometry.x, row.geometry.y),
            xytext=(5, 5),
            textcoords="offset points",
        )

    watershed.plot(
        ax=ax,
        alpha=0.7,
    )

    watershed.boundary.plot(
        ax=ax,
        color="red",
    )

    ctx.add_basemap(
        ax,
        source=ctx.providers.OpenTopoMap,
    )

    ax.set_title("Topographic map")
    ax.set_xlabel("Web Mercator X")
    ax.set_ylabel("Web Mercator Y")
    ax.set_aspect("equal")


def plot_watershed_stations_dem(
    points: gpd.GeoDataFrame,
    gauge: gpd.GeoDataFrame,
    watershed: gpd.GeoDataFrame,
    dem: np.ndarray,
    dem_crs,
    dem_transform,
    ax: plt.Axes,
    ) -> None:

    watershed = watershed.to_crs(dem_crs)
    gauge = gauge.to_crs(dem_crs)
    points= points.to_crs(dem_crs)

    assert watershed.crs == gauge.crs == points.crs
    
    extent = plotting_extent(
        dem,
        transform=dem_transform,
    )

    im = ax.imshow(
        dem,
        extent=extent,
        cmap="terrain",
    )

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

    points.plot(
        ax=ax,
        color="red",
        markersize=50,
    )

    for _, row in points.iterrows():
        ax.annotate(
            text=f"Weather station:\n{row['name']}",
            xy=(row.geometry.x, row.geometry.y),
            xytext=(-40, -35),
            textcoords="offset points",
        )

    watershed.plot(
        ax=ax,
        facecolor="none",
        edgecolor="red",
        linewidth=1.5,
    )

    fig = ax.get_figure()

    fig.colorbar(
        im,
        ax=ax,
        label="Elevation [m]",
    )

    ax.set_title("Digital elevation model")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_aspect("equal")


def plot_watershed_overview(
    points: gpd.GeoDataFrame,
    gauge: gpd.GeoDataFrame,
    watershed: gpd.GeoDataFrame,
    dem: np.ndarray,
    dem_crs,
    dem_transform,
    ) -> figure:

    fig, axs = plt.subplots(
        ncols=2,
        figsize=(16, 8),
    )

    plot_watershed_stations(
        points=points,
        watershed=watershed,
        ax=axs[0],
    )

    plot_watershed_stations_dem(
        points=points,
        gauge=gauge,
        watershed=watershed,
        dem=dem,
        dem_crs=dem_crs,
        dem_transform=dem_transform,
        ax=axs[1],
    )
    
    fig.suptitle(
        "Klingbach catchment: DEB10810, Herxheim",
        fontsize=14,
    )

    fig.tight_layout()
    plt.show()

    return fig
    

def plot_landuse(
    filepath: str | Path,
    ) -> figure:
    
    labels = ["Artificial surfaces", "Agricultural areas", "Forests and\nseminatural areas"] 
    
    df = read_landuse_csv(
        filepath=filepath,
    )

    df_plot = df.drop(columns=["gauge_id"]).loc[:, (df != 0).any(axis=0)]

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.bar(x=labels, height=df_plot.iloc[0])
    ax.set_ylabel("Proportion [%]")
    
    plt.tight_layout()
    plt.show()
    
    return fig