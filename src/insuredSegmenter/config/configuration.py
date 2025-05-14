from insuredSegmenter.entity.config_entity import DataIngestionConfig , DataTransformationConfig, PreparBaseModelConfig ,TrainingConfig
from insuredSegmenter.constants import *
from insuredSegmenter.utils.common import create_directories, read_yaml

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(str(config_filepath))
        self.params = read_yaml(str(params_filepath))

        create_directories([self.config.artifacts_root])
   

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        print(config.root_dir)
        print(config.sas)
        print(config.csv)
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            sas_data_path=config.sas,
            csv_data_path=config.csv
        )

        return data_ingestion_config

    def get_transformation_config(self) -> DataTransformationConfig:
        transforming_data_path = self.config.data_ingestion.csv
        transformation = self.config.data_transformation
        transformed_data_path = transformation.transformed_data_path
        transforer_path = transformation.transformer_path
        metric_features = transformation.metric_features
        non_metric_features = transformation.non_metric_features
        
        
        create_directories([transformation.root_dir])
    
        # create_directories([transformation.root_dir])
        transformation_config = DataTransformationConfig(
            root_dir= Path(transformation.root_dir),
            transforming_data_path= Path(transforming_data_path),
            transformed_data_path= Path(transformed_data_path),
            transformer_path= Path(transforer_path),
            metric_features= metric_features,
            non_metric_features= non_metric_features
            
        )
        return transformation_config
    
    def get_base_model_config(self) -> PreparBaseModelConfig:
        config = self.config.prepare_base_model
        
        create_directories([config.root_dir])
        
        prepare_base_model_config = PreparBaseModelConfig( 
              root_dir = Path(config.root_dir),
              base_model_path = Path(config.base_model_path),
              params_n_clusters = int(self.params.Kmeans.n_clusters),
              
        )
        return prepare_base_model_config  
    
    def get_training_config(self) -> TrainingConfig:
        training = self.config.train_model
        prepare_base_model = self.config.prepare_base_model
        params = self.params.kmeans
        training_data_path = self.config.data_transformation.transformed_data_path
        
        create_directories([training.root_dir])
        training_config = TrainingConfig(
            root_dir= Path(training.root_dir),
            base_model_path= Path(prepare_base_model.base_model_path),
            trained_model_path=Path(training.trained_model_path),
            training_data_path=Path(training_data_path),
            param_n_clusters=params.n_clusters
        )
        return training_config
    
