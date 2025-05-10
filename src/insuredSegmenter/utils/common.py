import os 
import yaml
from insuredSegmenter import logger
import joblib 
import json
from pathlib import Path 
from ensure import ensure_annotations
from box import ConfigBox
from typing import Any


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