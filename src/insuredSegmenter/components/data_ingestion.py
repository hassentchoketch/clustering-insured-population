import os
import pandas as pd
from insuredSegmenter.config.configuration import DataIngestionConfig
from insuredSegmenter import logger

class DataIngestion:
    """Data Ingestion"""
    def __init__(self, config: DataIngestionConfig):
        self.config = config # set config attribute to the class instance

    def initiate_data_ingestion(self):
        """ This function is responsible for data ingestion.
        It reads the sas data from the source  and  saves them as csv in spesified directory."""
        logger.info(f"Reading data from {self.config.sas_data_path} to {self.config.csv_data_path}")
        try: 
            df = pd.read_sas(self.config.sas_data_path) # read the data from the source path
            logger.info(f"Data read from {self.config.sas_data_path} successfully")
            
            df.to_csv(os.path.join(self.config.csv_data_path), index=False) # save the data to the root directory
            logger.info(f"Data saved to {self.config.root_dir} successfully")
        except Exception as e:
            logger.error(f"Error occurred while reading data from {self.config.source_path}: {e}")
            raise e

    
        
    