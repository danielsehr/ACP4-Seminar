from dataclasses import dataclass, field

@dataclass
class Config:
    fid: int = 1193
    gauge_id: str = "DEB10810"
    
    catchment_dir: str = "data/camels_de/CAMELS_DE_catchment_boundaries/catchments"
    catchment_gpkg_path: str = "data/camels_de/CAMELS_DE_catchment_boundaries/catchments/CAMELS_DE_catchments.gpkg"
    
    timeseries_dir: str = "data/camels_de/timeseries"    
    agrometeo_dir: str = "data/agrarmeteorologie_stations"

# class Excercise1Config:
#     catchment_dir: str = "data/camels_de/CAMELS_DE_catchment_boundaries/catchments"
#     catchment_gpkg_path: str = "data/camels_de/CAMELS_DE_catchment_boundaries/catchments/CAMELS_DE_catchments.gpkg"
#     fid: int = 1193
#     gauge_id: str = "DEB10810"
    
#     agrometeo_dir: str = "data/agrarmeteorologie_stations"
#     herxheimweyher_lon_lat: tuple = ("Herxheimweyher", 8.25, 49.16)
#     steinweiler_lon_lat: tuple = ("Steinweiler", 8.10, 49.10)


# @dataclass
# class Excercise2Config:
#     timeseries_dir: str = "data/camels_de/timeseries"
    
# @dataclass
# class Config:
#     excercise1: Excercise1Config = field(default_factory=Excercise1Config)
#     excercise2: Excercise2Config = field(default_factory=Excercise2Config)
    
