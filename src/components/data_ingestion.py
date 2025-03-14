# Import necessary libraries and modules
import os
import sys
from src.exception import CustomException  # Custom exception handling
from src.logger import logging  # Logging module for tracking
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass  # For creating configuration classes

# Import data transformation and model training components
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainer, ModelTrainerConfig

# Configuration class for data ingestion paths using dataclass decorator for simplicity
@dataclass
class DataIngestionConfig:
    # Default paths for output files (using OS path joining)
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

# Main class responsible for data ingestion
class DataIngestion:
    def __init__(self):
        # Initialize with the configuration class
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        """
        Main method to execute data ingestion process:
        1. Read source data
        2. Split into train/test sets
        3. Save raw data and splits
        4. Return paths for downstream processes
        """
        logging.info("Entered the data ingestion method or component")
        try:
            # Read source data from CSV
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info('Read the dataset as dataframe')

            # Create directory structure if it doesn't exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Save raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Saved raw data")

            # Split data into train/test sets (80/20 split)
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save split datasets
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Data ingestion completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            # Use custom exception handling with error propagation
            raise CustomException(e, sys)

# Main execution block when script is run directly
if __name__ == "__main__":
    # 1. Data Ingestion
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    # 2. Data Transformation
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    # 3. Model Training
    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))