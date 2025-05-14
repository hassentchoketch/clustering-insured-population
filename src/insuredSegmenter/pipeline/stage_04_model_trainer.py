from insuredSegmenter.config.configuration import ConfigurationManager
from insuredSegmenter.components.model_trainer import Training
from insuredSegmenter import logger 


STAGE_NAME = "Training Stage"

class TrainingPipeline:
    def __init__(self):
        self.config = ConfigurationManager()
        self.training_config = self.config.get_training_config()
        self.training = Training(config=self.training_config)

    def start_training(self):
        self.training.get_base_model()
        self.training.train_model()
        
        
if __name__ == "__main__":
    try:
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n\n")
        logger.info("Starting training stage")
        training = TrainingPipeline()
        training.start_training()
        logger.info("Training stage completed")
    except Exception as e:
        logger.error(f"Error occurred in Training stage: {e}")
        raise e