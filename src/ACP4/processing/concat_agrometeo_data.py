from pathlib import Path
import pandas as pd

from src.acp4.config.config import Config
config = Config()


paths = [
    config.agrometeo_herxheimweyher_dir,
    config.agrometeo_steinweiler_dir
]

def concat_agrometeo_data(
    paths: list[str] | list[Path] = paths
    ) -> None:
    
    for path in paths:
        files = sorted(list(Path(path).glob("*.csv")))
        
        output_dir = Path(path)
        output_path = output_dir / f"{output_dir.stem}_concat.csv"

        df = pd.concat(
            [pd.read_csv(file, sep=";", decimal=",") for file in files],
            axis=0
        )

        if output_path.exists():
            print("Files yet exists.")
            return
        
        df.to_csv(
            output_path, 
            sep=";", 
            index=False
            )