from dataclasses import dataclass

@dataclass
class Config:
    fid: int = 1193
    gauge_id: str = "DEB10810"
    
    catchment_dir: str = "data/camels_de/CAMELS_DE_catchment_boundaries/catchments"
    catchment_gpkg_path: str = "data/camels_de/CAMELS_DE_catchment_boundaries/catchments/CAMELS_DE_catchments.gpkg"
    dem_asc_path: str = "data/mapping_files/dgm200_utm32s.asc"
    gauge_gpkg_path: str = "data/camels_de/CAMELS_DE_catchment_boundaries/gauging_stations/CAMELS_DE_gauging_stations.gpkg"
    landcover_csv_path: str = "data/camels_de/CAMELS_DE_landcover_attributes.csv"
    
    timeseries_dir: str = "data/camels_de/timeseries"    
    timeseries_simulated_dir: str = "data/camels_de/timeseries_simulated"    
    agrometeo_dir: str = "data/agrarmeteorologie_stations"
    agrometeo_steinweiler_dir: str = "data/agrarmeteorologie_stations/steinweiler"
    agrometeo_herxheimweyher_dir: str = "data/agrarmeteorologie_stations/herxheimweyher"

    agrometeo_points: tuple = (("Herxheimweyher", 8.25, 49.16),
                               ("Steinweiler", 8.10, 49.10))

    solar_constant: float = 0.0820 #  MJ m-2 min-1
    

# @dataclass
# class Excercise2Config:
#     timeseries_dir: str = "data/camels_de/timeseries"
    
# @dataclass
# class Config:
#     excercise1: Excercise1Config = field(default_factory=Excercise1Config)
#     excercise2: Excercise2Config = field(default_factory=Excercise2Config)
    
