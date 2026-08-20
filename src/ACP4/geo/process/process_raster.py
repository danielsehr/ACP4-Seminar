import numpy as np
import geopandas as gpd

import rasterio
from rasterio.mask import mask
import rasterio.transform

from typing import Any


def expand_bbox(
    gdf: gpd.GeoDataFrame,
    extent: float,
) -> tuple[float, float, float, float]:
    
    gdf = gdf.to_crs("25832")
    
    centroid = gdf.geometry.centroid
    
    return (
        centroid.x.iloc[0] - extent,
        centroid.y.iloc[0] - extent,
        centroid.x.iloc[0] + extent,
        centroid.y.iloc[0] + extent,
    )
    





