from insuredSegmenter.config.configuration import ConfigurationManager
from insuredSegmenter.components.prepare_base_model import PrepareBaseModel
from insuredSegmenter import logger 


STAGE_NAME = "Prepare Base Model Stage"

class PrepareBaseModelPipeline:
    def __init__(self):
        self.config = ConfigurationManager()
        self.prepare_base_model_config = self.config.get_base_model_config()
        self.prepare_base_model = PrepareBaseModel(config=self.prepare_base_model_config)

    def start_prepare_base_model(self):
        self.prepare_base_model.get_base_model()
        
        
if __name__ == "__main__":
    try:
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n\n")
        logger.info("Starting prepare base model stage")
        prepare_base_model_pipeline = PrepareBaseModelPipeline()
        prepare_base_model_pipeline.start_prepare_base_model()
        logger.info("Prepare base model stage completed")
    except Exception as e:
        logger.error(f"Error occurred in prepare base model stage: {e}")
        raise e