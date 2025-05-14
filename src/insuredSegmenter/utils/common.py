import os 
import yaml
from insuredSegmenter import logger
import joblib 
import json
from pathlib import Path 
from ensure import ensure_annotations
from box import ConfigBox
from typing import Any
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.base import BaseEstimator, TransformerMixin
import pickle



@ensure_annotations
def read_yaml(file_path: str) -> ConfigBox:
    """
    Load a YAML file and return its contents as a ConfigBox object.
    
    Args:
        file_path (str): Path to the YAML file.
        
    Returns:
        ConfigBox: Contents of the YAML file as a ConfigBox object.
    """
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"YAML file loaded successfully: {file_path}")
        return ConfigBox(config)
    except Exception as e:
        logger.error(f"Error loading YAML file: {e}")
        raise e

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")
        
@ensure_annotations
def save_json(file_path: str, data: dict) -> None:
    """
    Save a dictionary to a JSON file.
    
    Args:
        file_path (str): Path to the JSON file.
        data (dict): Dictionary to save.
        
    Returns:
        None
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            logger.info(f"JSON file saved successfully: {file_path}")
    except Exception as e:
        logger.error(f"Error saving JSON file: {e}")
        raise e
    
@ensure_annotations
def load_json(file_path: str) -> dict:
    """
    Load a JSON file and return its contents as a dictionary.
    
    Args:
        file_path (str): Path to the JSON file.
        
    Returns:
        dict: Contents of the JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            logger.info(f"JSON file loaded successfully: {file_path}")
        return ConfigBox(data)
    except Exception as e:
        logger.error(f"Error loading JSON file: {e}")
        raise e
    
@ensure_annotations
def save_bin(file_path: str, data: Any) -> None:
    """
    Save data to a binary file using joblib.
    
    Args:
        file_path (str): Path to the binary file.
        data (Any): Data to save.
        
    Returns:
        None
    """
    try:
        joblib.dump(data, file_path)
        logger.info(f"Binary file saved successfully: {file_path}")
    except Exception as e:
        logger.error(f"Error saving binary file: {e}")
        raise e
    
@ensure_annotations
def load_bin(file_path: str) -> Any:
    """
    Load data from a binary file using joblib.
    
    Args:
        file_path (str): Path to the binary file.
        
    Returns:
        Any: Loaded data.
    """
    try:
        data = joblib.load(file_path)
        logger.info(f"Binary file loaded successfully: {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading binary file: {e}")
        raise e

@ensure_annotations
def get_size(file_path: str) -> int:
    
    """
    Get the size of a file in Kbytes.
    
    Args:
        file_path (str): Path to the file.
        
    Returns:
        int: Size of the file in bytes.
    """
    try:
        size = round(os.path.getsize(file_path)/1024)
        logger.info(f"File size: {size} Kbytes")
        return size
    except Exception as e:
        logger.error(f"Error getting file size: {e}")
        raise e
    
@ensure_annotations
def _load_object(file_path: Path):
        """
        This function is used to load a pickled object from the specified path.
        """
        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            raise (e)

class OutlierRemover(BaseEstimator, TransformerMixin):
    """
    Custom transformer to remove outliers using Z-score method.
    This implements scikit-learn's transformer interface.
    """
    def __init__(self, z_threshold=3.0):
        self.z_threshold = z_threshold
        self.feature_indices_ = None
        
    def fit(self, X, y=None):
        # Store indices of features with outliers to be used in transform
        return self
        
    def transform(self, X):
        if isinstance(X, pd.DataFrame):
            X_transformed = X.copy()
            # Apply z-score thresholding to each column
            for col in X_transformed.columns:
                if X_transformed[col].dtype in [np.float64, np.int64]:
                    z_scores = np.abs(stats.zscore(X_transformed[col], nan_policy='omit'))
                    X_transformed.loc[z_scores >= self.z_threshold, col] = np.nan
            return X_transformed
        else:
            # If not DataFrame, convert to numpy array
            X_transformed = np.copy(X)
            # Apply z-score thresholding to each column
            for col in range(X_transformed.shape[1]):
                z_scores = np.abs(stats.zscore(X_transformed[:, col], nan_policy='omit'))
                X_transformed[z_scores >= self.z_threshold, col] = np.nan
            return X_transformed

class SkewnessTransformer(BaseEstimator, TransformerMixin):
    """
    Custom transformer to handle skewed data automatically.
    Applies log transformation to highly skewed features.
    """
    def __init__(self, skew_threshold=1.0):
        self.skew_threshold = skew_threshold
        self.skewed_features_ = {}  # Will store skewed features and their min values
    
    def fit(self, X, y=None):
        # Identify skewed features
        if isinstance(X, pd.DataFrame):
            for col in X.columns:
                if X[col].dtype in [np.float64, np.int64]:
                    skewness = X[col].skew()
                    if abs(skewness) > self.skew_threshold:
                        # Store min value to use in transformation
                        min_val = X[col].min()
                        self.skewed_features_[col] = min_val
        else:
            # For numpy arrays, we'll transform all numeric columns
            for col in range(X.shape[1]):
                if np.issubdtype(X[:, col].dtype, np.number):
                    # Use pandas Series for skew calculation
                    skewness = pd.Series(X[:, col]).skew()
                    if abs(skewness) > self.skew_threshold:
                        min_val = np.min(X[:, col])
                        self.skewed_features_[col] = min_val
        return self
    
    def transform(self, X):
        X_transformed = X.copy() if isinstance(X, pd.DataFrame) else np.copy(X)
        
        if isinstance(X, pd.DataFrame):
            for col, min_val in self.skewed_features_.items():
                if col in X_transformed.columns:
                    # Apply log transformation (adding small constant to handle zeros)
                    X_transformed[col] = np.log1p(X_transformed[col] - min_val + 0.01)
        else:
            for col, min_val in self.skewed_features_.items():
                # Apply log transformation to numpy array
                X_transformed[:, col] = np.log1p(X_transformed[:, col] - min_val + 0.01)
                
        return X_transformed
