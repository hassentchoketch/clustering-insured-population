from insuredSegmenter.config.configuration import ConfigurationManager
from insuredSegmenter.config.configuration import DataTransformationConfig
from pathlib import Path
import pandas as pd
import pickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer, StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from insuredSegmenter.utils.common import OutlierRemover, SkewnessTransformer

from insuredSegmenter import logger


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        
    def _save_object(self, obj, file_path: Path):
        """
        This function is used to save the object to the specified path.
        """
        try:
            with open(file_path, 'wb') as file:
                pickle.dump(obj, file)
        except Exception as e:
            raise (e)
    
    def get_data_transformer_object(self, remove_outliers: bool = True) -> Pipeline:
        """
        This function is used to transform the data using the following steps:
        1. remove outliers from numerical columns (optional)
        2. handle skewed numerical features
        3. impute missing values with median for numerical columns
        4. transform numerical data using PowerTransformer
        5. impute missing values with most frequent value for categorical columns
        6. one-hot encode categorical data
        
        The entire transformation is wrapped in a single Pipeline for easy saving and reuse.
        """
        try:
            # Define the preprocessor steps
            preprocessing_steps = []
            
            # Step 1: Add outlier removal if requested
            if remove_outliers:
                preprocessing_steps.append(("outlier_remover", OutlierRemover(z_threshold=3.0)))
                
            # Step 2: Add skewness transformer
            preprocessing_steps.append(("skewness_transformer", SkewnessTransformer(skew_threshold=1.0)))
            
            # Step 3: Column transformer for different column types
            num_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),  # impute missing values with median
                ("power_transform", PowerTransformer(standardize=False)),  # additional handling for skewed data
                ("scaler", StandardScaler())  # scale the data
            ])
            
            cat_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),  # impute missing values with most frequent value
                ("onehotencoder", OneHotEncoder(handle_unknown='ignore')),  # one hot encode the categorical variables
                ("scaler", StandardScaler(with_mean=False))  # scale the data (with_mean=False for sparse matrices)
            ])
            
            column_transformer = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, self.config.metric_features),
                    ("cat_pipeline", cat_pipeline, self.config.non_metric_features)
                ]
            )
            
            preprocessing_steps.append(("column_transformer", column_transformer))
            
            # Create the full pipeline
            preprocessor = Pipeline(preprocessing_steps)
            
            return preprocessor
            
        except Exception as e:
            raise (e)
    
    def initiate_data_transformation(
        self, 
        transforming_data_path: Path, 
        remove_outliers: bool = True,
        save_transformer: bool = True
        ) -> pd.DataFrame:
        """
        This function is responsible for transforming the data.
        
        Args:
            transforming_data_path: Path to the CSV file to transform
            numerical_columns: List of numerical column names
            categorical_columns: List of categorical column names
            remove_outliers: Whether to remove outliers (default: True)
            save_transformer: Whether to save the transformer for later use (default: True)
            
        Returns:
            Transformed data
        """
        try:
            # read the data from the specified path
            df = pd.read_csv(transforming_data_path)
            
            # get the data transformer object with outlier removal integrated into the pipeline
            data_transformer = self.get_data_transformer_object( remove_outliers)
            
            # transform the data
            transformed_data = data_transformer.fit_transform(df)
            
            # save the transformed data
            self._save_object(transformed_data, self.config.transformed_data_path)
            
            # save the transformer if requested
            if save_transformer:
                self._save_object(data_transformer, self.config.transformer_path)
            
            return transformed_data
        
        except Exception as e:
            raise (e)