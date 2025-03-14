"""
Prediction pipeline components:
- PredictPipeline: Handles model loading and prediction execution
- CustomData: Structures input data for predictions
"""

import sys
import os  # Required for path operations
import pandas as pd
from src.exception import CustomException
from src.utils import load_object


class PredictPipeline:
    """Handles model loading and makes predictions using trained artifacts"""
    
    def __init__(self):
        """Initialize prediction pipeline (no current initialization needed)"""
        pass

    def predict(self, features):
        """
        Makes prediction using pre-trained model and preprocessor
        
        Args:
            features (DataFrame): Input data for prediction
            
        Returns:
            array: Model predictions
            
        Raises:
            CustomException: If any error occurs during prediction
        """
        try:
            # Define paths to trained artifacts (assumes artifacts/ directory exists)
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            
            # Debugging logs can be removed in production
            print("Before Loading")
            
            # Load trained model and preprocessor from pickle files
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            
            print("After Loading")
            
            # Apply preprocessing to input data
            data_scaled = preprocessor.transform(features)
            
            # Generate predictions using preprocessed data
            preds = model.predict(data_scaled)
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    """Encapsulates and validates input data for prediction requests"""
    
    def __init__(self,
                 gender: str,
                 race_ethnicity: str,
                 parental_level_of_education: str,
                 lunch: str,
                 test_preparation_course: str,
                 reading_score: int,
                 writing_score: int):
        """
        Initialize input data attributes
        
        Args:
            gender: Student's gender
            race_ethnicity: Student's ethnic group
            parental_level_of_education: Parents' education level
            lunch: Student's lunch type
            test_preparation_course: Test prep course completion status
            reading_score: Reading test score
            writing_score: Writing test score
        """
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        """
        Converts input data attributes to pandas DataFrame format
        
        Returns:
            DataFrame: Input data structured for model prediction
            
        Raises:
            CustomException: If conversion to DataFrame fails
        """
        try:
            # Structure data as dictionary for DataFrame conversion
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            # Create single-row DataFrame matching model input format
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)