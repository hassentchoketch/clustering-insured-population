from insuredSegmenter.entity.config_entity import TrainingConfig
from pathlib import Path 
import joblib
import pickle   

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
    def _load_object(self, file_path: Path):
        """
        This function is used to load a pickled object from the specified path.
        """
        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            raise (e)
    
    def get_base_model(self):
        # Load the base model
        self.model = joblib.load(self.config.base_model_path)
        
    def train_model(self):
        # Load the training data
        training_data = self._load_object(self.config.training_data_path)
        
        # Extract features and labels
        X = training_data
        # Train the KMeans model
        self.model.fit(X)
        self._save_model(path=self.config.trained_model_path)
        
    def _save_model(self,path: Path) :
        # Save the trained model to the specified path
        joblib.dump(self.model,path )
        
