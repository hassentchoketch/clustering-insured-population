from insuredSegmenter.entity.config_entity import DataIngestionConfig , PreparBaseModelConfig
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

    def get_base_model_config(self) -> PreparBaseModelConfig:
        config = self.config.prepare_base_model
        
        create_directories([config.root_dir])
        
        prepare_base_model_config = PreparBaseModelConfig( 
              root_dir = Path(config.root_dir),
              base_model_path = Path(config.base_model_path),
              params_n_clusters = int(self.params.Kmeans.n_clusters),
              
        )
        return prepare_base_model_config  