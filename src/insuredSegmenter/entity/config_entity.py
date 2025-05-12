from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    """
    Data Ingestion Configuration
    """
    root_dir: Path
    sas_data_path: Path
    csv_data_path: Path
    
@dataclass
class PreparBaseModelConfig:
    """
    Base class for all model configurations.
    """
    root_dir : Path 
    base_model_path : Path
    params_n_clusters : int