from insuredSegmenter.config.configuration import ConfigurationManager
from insuredSegmenter.entity.config_entity import PreparBaseModelConfig
from insuredSegmenter.constants import *
from sklearn.cluster import KMeans
import joblib
from typing import Any
from insuredSegmenter import logger




class PrepareBaseModel:
    def __init__(self, config: PreparBaseModelConfig):
        self.config = config
        self.model = None
    
    def get_base_model(self) -> KMeans:
        """
        Create and save a KMeans base model based on configuration.
        
        Returns:
            KMeans: Initialized KMeans model
        """
        self.model = KMeans(
            n_clusters=self.config.params_n_clusters,
            random_state=42,
            # Add other necessary KMeans parameters here
        )
        
        # Save the model
        self.save_base_model()
        return self.model
    
    def load_base_model(self) -> Any:
        """
        Load a pre-saved base model from the specified path.
        
        Returns:
            Any: Loaded model
        """
        try:
            logger.info(f"Loading base model from {self.config.base_model_path}")
            self.model = joblib.load(str(self.config.base_model_path))
            logger.info("Base model loaded successfully")
            return self.model
        except FileNotFoundError as e:
            logger.error(f"Model file not found: {e}")
            raise
    
    def save_base_model(self) -> None:
        """
        Save the current model to the specified path.
        """
        if self.model is None:
            raise ValueError("No model to save. Call get_base_model() first.")
        
        if not self.config.base_model_path:
            
            raise ValueError("Base model path is not specified")
        
        try:
            logger.info(f"Saving base model to {self.config.base_model_path}"),
            joblib.dump(self.model, str(self.config.base_model_path)),
            logger.info(f"Base model saved successfully to {self.config.base_model_path}"),
        except Exception as e:
            logger.exception(f"Error saving base model to {self.config.base_model_path}: {e}"),
            raise