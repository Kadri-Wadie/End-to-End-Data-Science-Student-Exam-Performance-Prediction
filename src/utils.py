# utils.py

"""
Utility functions for model training, evaluation, and serialization.
Includes methods to save/load objects and evaluate multiple models with hyperparameter tuning.
"""

import os
import sys
import numpy as np 
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from src.exception import CustomException


def save_object(file_path, obj):
    """
    Saves a Python object to the specified file path using pickle serialization.
    Automatically creates directories if they don't exist.

    Args:
        file_path (str): Path to the file where the object will be saved
        obj (object): Python object to be saved

    Raises:
        CustomException: If any error occurs during the saving process
    """
    try:
        # Create directory structure if not exists
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        # Serialize and save the object
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    """
    Evaluates multiple machine learning models using GridSearchCV for hyperparameter tuning.
    Returns test set R² scores for all models.

    Args:
        X_train (pd.DataFrame): Training features
        y_train (pd.Series): Training target
        X_test (pd.DataFrame): Testing features
        y_test (pd.Series): Testing target
        models (dict): Dictionary of model instances to evaluate
        param (dict): Dictionary of hyperparameter grids for each model

    Returns:
        dict: Model names as keys and corresponding test R² scores as values

    Raises:
        CustomException: If any error occurs during model evaluation
    """
    try:
        report = {}

        for i in range(len(list(models))):
            # Get model and parameters from dictionary
            model_name = list(models.keys())[i]
            model = list(models.values())[i]
            para = param[model_name]

            # Hyperparameter tuning with GridSearchCV
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            # Update model with best parameters and retrain
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            # Generate predictions and calculate scores
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            train_score = r2_score(y_train, y_train_pred)
            test_score = r2_score(y_test, y_test_pred)

            # Store test score in report
            report[model_name] = test_score

        return report

    except Exception as e:
        raise CustomException(e, sys)
    

def load_object(file_path):
    """
    Loads a serialized Python object from a file using pickle.

    Args:
        file_path (str): Path to the serialized object file

    Returns:
        object: Deserialized Python object

    Raises:
        CustomException: If any error occurs during loading
    """
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
        
    except Exception as e:
        raise CustomException(e, sys)