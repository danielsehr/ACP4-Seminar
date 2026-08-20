from pathlib import Path
import numpy as np

import geopandas as gpd
from shapely import Point
import rasterio
from rasterio.windows import from_bounds
from rasterio.mask import mask

from typing import Any


def read_catchment(
    filepath: str | Path,
    gauge_id: str
    ) -> gpd.GeoDataFrame:

    gdf = gpd.read_file(filename=filepath)
    gdf = gdf[gdf["gauge_id"] == gauge_id]
    
    return gdf


def read_gauge_station(
    filepath: str | Path,
    gauge_id: str
    ) -> gpd.GeoDataFrame:
    
    gdf = gpd.read_file(filename=filepath)
    gdf = gdf[gdf["gauge_id"] == gauge_id]
    
    return gdf
    
    
def create_weatherstation_points(
    points: list[tuple] | tuple[tuple]
    ) -> gpd.GeoDataFrame:

    points_gdf = gpd.GeoDataFrame(
    [
        {
            "name": name,
            "geometry" : Point(lon, lat)
        } 
        for name, lon, lat in points
    ],
    crs="EPSG:4326",
    )
    
    return points_gdf


def read_dem_window(
    filepath: str | Path,
    bbox: tuple[float, float, float, float],
    ) -> tuple[np.ndarray, Any, Any]:
    
    with rasterio.open(filepath) as src:
        dem_crs = src.crs
        minx, miny, maxx, maxy = bbox

        window = from_bounds(
            minx,
            miny,
            maxx,
            maxy,
            transform=src.transform,
        )

        dem = src.read(1, window=window, masked=True)
        transform = src.window_transform(window)
        
        return dem, transform, dem_crs
    