from insuredSegmenter.config.configuration import ConfigurationManager
from insuredSegmenter.components.data_ingestion import DataIngestion
from insuredSegmenter import logger


STAGE_NAME = "Data Ingestion Stage"
logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n\n")

class DataIngestionPipeline:
    def __init__(self):
        self.config = ConfigurationManager()
        self.data_ingestion_config = self.config.get_data_ingestion_config()
        self.data_ingestion = DataIngestion(config=self.data_ingestion_config)

    def start_data_ingestion(self):
        self.data_ingestion.initiate_data_ingestion()

        

if __name__ == "__main__":
    try:
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n\n")
        logger.info("Starting data ingestion stage")
        data_ingestion_pipeline = DataIngestionPipeline()
        data_ingestion_pipeline.start_data_ingestion()
        logger.info("Data ingestion stage completed")
    except Exception as e:
        logger.error(f"Error occurred in data ingestion stage: {e}")
        raise e
    
    
    
        
    