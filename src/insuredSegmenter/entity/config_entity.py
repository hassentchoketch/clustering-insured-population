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
 
@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    transformed_data_path: Path
    transforming_data_path: Path
    transformer_path : Path 
    metric_features : list
    non_metric_features : list   
    
@dataclass
class PreparBaseModelConfig:
    """
    Base class for all model configurations.
    """
    root_dir : Path 
    base_model_path : Path
    params_n_clusters : int
    
@dataclass(frozen=True) # frozen=True makes the dataclass immutable
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
    base_model_path: Path
    training_data_path: Path
    param_n_clusters: int
    
    
@dataclass
class ModelEvaluationConfig:
    """
    Class to hold the evaluation results of a model.
    """
    root_dir: Path
    transformed_data_path: Path
    model_path: Path
    all_params: dict
    metric_file_name: Path
    visualisation_path: Path