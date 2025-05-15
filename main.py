from insuredSegmenter.pipeline.stage_01_data_igestion import DataIngestionPipeline
from insuredSegmenter.pipeline.stage_02_data_transformation import DataTransformationPipeline
from insuredSegmenter.pipeline.stage_03_prepare_base_model import PrepareBaseModelPipeline 
from insuredSegmenter.pipeline.stage_04_model_trainer import TrainingPipeline  
from insuredSegmenter.pipeline.stage_05_model_evaluation import EvaluationPipeline
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

STAGE_NAME = "Data Transformation Stage"

try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n\n")
    logger.info("Starting data Transformation stage")
    data_ingestion_pipeline = DataTransformationPipeline()
    data_ingestion_pipeline.start_data_transformation()
    logger.info("Data Transformation stage completed")
except Exception as e:
    logger.error(f"Error occurred in data Transformation stage: {e}")
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


STAGE_NAME = "Training Stage"

try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n\n")
    logger.info("Starting training stage")
    training_pipline = TrainingPipeline()
    training_pipline.start_training()
    logger.info("Training stage completed")
except Exception as e:
    logger.error(f"Error occurred in training stage: {e}")
    raise e

STAGE_NAME = "Evaluation Stage"

try:
    logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n\n")
    logger.info("Starting evaluation stage")
    evaluation = EvaluationPipeline()
    evaluation.start_evaluation()
    logger.info("Evaluation stage completed")
except Exception as e:
    logger.error(f"Error occurred in Evaluation stage: {e}")
    raise e