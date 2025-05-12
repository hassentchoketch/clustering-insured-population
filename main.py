from insuredSegmenter.pipeline.stage_01_data_igestion import DataIngestionPipeline
from insuredSegmenter.pipeline.stage_02_prepare_base_model import PrepareBaseModelPipeline     
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

STAGE_NAME = "Prepare Base Model Stage"
 

try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n\n")
    logger.info("Starting prepare base model stage")
    prepare_base_model_pipeline = PrepareBaseModelPipeline()
    prepare_base_model_pipeline.start_prepare_base_model()
    logger.info("Prepare base model stage completed")
except Exception as e:
    logger.error(f"Error occurred in prepare base model stage: {e}")
    raise e