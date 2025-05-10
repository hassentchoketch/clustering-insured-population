from insuredSegmenter.pipeline.stage_01_data_igestion import DataIngestionPipeline
from insuredSegmenter import logger


STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n\n")
    logger.info("Starting data ingestion stage")
    data_ingestion_pipeline = DataIngestionPipeline()
    data_ingestion_pipeline.start_data_ingestion()
    logger.info("Data ingestion stage completed")
except Exception as e:
    logger.error(f"Error occurred in data ingestion stage: {e}")
    raise e