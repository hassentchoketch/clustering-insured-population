from insuredSegmenter.config.configuration import ConfigurationManager
from insuredSegmenter.components.model_evaluation import ModelEvaluation
from insuredSegmenter import logger 


STAGE_NAME = "Model evaluation Stage"

class EvaluationPipeline:
    def __init__(self):
        self.config = ConfigurationManager()
        self.evaluation_config = self.config.get_model_evaluation_config()
        self.evaluation = ModelEvaluation(config=self.evaluation_config)

    def start_evaluation(self):
        self.evaluation.save_results()

        
        
if __name__ == "__main__":
    try:
        logger.info(f"\n\n{'*'*20} {STAGE_NAME} {'*'*20}\n\n")
        logger.info("Starting evaluation stage")
        evaluation = EvaluationPipeline()
        evaluation.start_evaluation()
        logger.info("Evaluation stage completed")
    except Exception as e:
        logger.error(f"Error occurred in Evaluation stage: {e}")
        raise e