# Import required libraries and modules
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException  # Custom exception handling
from src.logger import logging  # Logging module for tracking
import os
from src.utils import save_object  # Utility function to save Python objects

# Configuration class for data transformation paths using dataclass
@dataclass
class DataTransformationConfig:
    # Default path for saving preprocessing object (serialized pipeline)
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        # Initialize with configuration class
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        Creates and returns a preprocessing pipeline that handles:
        - Numerical columns: Imputation + Scaling
        - Categorical columns: Imputation + Encoding + Scaling
        '''
        try:
            # Define column types
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Numerical data processing pipeline
            num_pipeline = Pipeline(
                steps=[
                    # Handle missing values with median imputation
                    ("imputer", SimpleImputer(strategy="median")),
                    # Standardize features by removing mean and scaling to unit variance
                    ("scaler", StandardScaler())
                ]
            )

            # Categorical data processing pipeline
            cat_pipeline = Pipeline(
                steps=[
                    # Replace missing values with most frequent category
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    # Convert categorical variables to one-hot numeric arrays
                    ("one_hot_encoder", OneHotEncoder()),
                    # Scale without centering to preserve sparsity
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # Combine pipelines using ColumnTransformer
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        '''
        Executes full data transformation process:
        1. Loads training and test data
        2. Splits into features and target
        3. Applies preprocessing pipelines
        4. Saves preprocessing object
        5. Returns processed numpy arrays
        '''
        try:
            # Load raw data from provided paths
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            # Get preprocessing pipeline object
            preprocessing_obj = self.get_data_transformer_object()

            # Configuration
            target_column_name = "math_score"  # Our prediction target
            numerical_columns = ["writing_score", "reading_score"]  # Used for validation

            # Split data into features (X) and target (y)
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on dataframes")

            # Apply preprocessing pipeline
            # Fit_transform on training, transform only on test to prevent data leakage
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine processed features with target values
            train_arr = np.c_[
                input_feature_train_arr,  # Processed features
                np.array(target_feature_train_df)  # Original target values
            ]
            test_arr = np.c_[
                input_feature_test_arr,
                np.array(target_feature_test_df)
            ]

            # Save preprocessing object for future use (inference)
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            logging.info("Preprocessing object saved successfully")

            return (
                train_arr,  # Processed training data (features + target)
                test_arr,   # Processed test data (features + target)
                self.data_transformation_config.preprocessor_obj_file_path,  # Path to saved pipeline
            )
        except Exception as e:
            raise CustomException(e, sys)