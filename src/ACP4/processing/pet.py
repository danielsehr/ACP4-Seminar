import numpy as np
import pandas as pd
from typing import Any

from acp4.config.config import Config
config = Config()


def convert_lat_to_radians(latitude: float) -> float:
    return (np.pi / 180) * latitude


def calc_inv_earthsun_distance(doy: int)-> float:
    return 1 + 0.033 * np.cos(((2 * np.pi) / 365) * doy)


def calc_solar_declination(doy: int)-> float:
    return 0.409 * np.sin(((2 * np.pi / 365) * doy) - 1.39)
    
    
def calc_sunset_hour_angle(
    solar_declination: float,
    lat_radians: float
    ) -> float:
    
    return( 
           np.arccos(
               np.clip(
                   -np.tan(lat_radians) * np.tan(solar_declination), -1.0, 1.0
                   )
               )
           )


def calc_daily_extraterr_radiation(
    doy: int,
    latitude: float,
    solar_constant: float
    ) -> float:
    
    inv_rel_sunearth_dist = calc_inv_earthsun_distance(doy=doy)
    lat_radians = convert_lat_to_radians(latitude=latitude)
    solar_declination = calc_solar_declination(doy=doy)
    
    sunset_hour_angle =  calc_sunset_hour_angle(
        solar_declination=solar_declination, 
        lat_radians=lat_radians
    )
    
    return (
        ((24 * 60) / np.pi)
        * solar_constant
        * inv_rel_sunearth_dist
        * (
            sunset_hour_angle 
            * np.sin(lat_radians) 
            * np.sin(solar_declination)
            
            + np.cos(lat_radians) 
            * np.cos(solar_declination) 
            * np.sin(sunset_hour_angle)
        )
    )
    

def calculate_hargreaves_pet(
    df: pd.DataFrame
    ) -> np.ndarray | pd.Series:
    
    doy=df.index.day_of_year
    latitude=config.agrometeo_points[0][2]
    solar_constant=config.solar_constant
    temperature_mean=df.temperature_mean
    temperature_min=df.temperature_min
    temperature_max=df.temperature_max
    
    daily_extraterr_radiation = calc_daily_extraterr_radiation(
        doy=doy,
        latitude=latitude,
        solar_constant=solar_constant
    )
    
    
    return (
        0.0023 * daily_extraterr_radiation 
        * (temperature_mean + 17.8) 
        * np.sqrt(temperature_max - temperature_min)
    )