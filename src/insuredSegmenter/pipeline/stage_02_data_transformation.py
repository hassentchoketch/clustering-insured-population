from insuredSegmenter.config.configuration import ConfigurationManager
from insuredSegmenter.components.data_transformation import DataTransformation
from insuredSegmenter import logger 


STAGE_NAME = "Prepare Base Model Stage"

class DataTransformationPipeline:
    def __init__(self):
        self.config = ConfigurationManager()
        self.data_transformation_config = self.config.get_transformation_config()
        self.data_transformation = DataTransformation(config=self.data_transformation_config)

    def start_data_transformation(self):
        self.data_transformation.get_data_transformer_object()
        self.data_transformation.initiate_data_transformation(self.data_transformation_config.transforming_data_path)
        
        
if __name__ == "__main__":
    try:
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n\n")
        logger.info("Starting data transformation stage")
        data_transformation_pipeline = DataTransformationPipeline()
        data_transformation_pipeline.start_data_transformation()
        logger.info("data transformation stage completed")
    except Exception as e:
        logger.error(f"Error occurred in data transformation stage: {e}")
        raise e