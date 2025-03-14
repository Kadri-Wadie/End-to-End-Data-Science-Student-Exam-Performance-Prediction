# Import necessary libraries and modules
import os
import sys
from dataclasses import dataclass

# Model imports
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

# Custom modules
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

# Configuration class using dataclass decorator
@dataclass
class ModelTrainerConfig:
    # Default path for saving trained models
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        # Initialize with configuration settings
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        """
        Main method to handle complete model training process
        
        Args:
            train_array (numpy.ndarray): Training data array
            test_array (numpy.ndarray): Testing data array
            
        Returns:
            float: R² score of the best performing model
            
        Raises:
            CustomException: If no suitable model is found
        """
        try:
            # Data Splitting
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],  # All columns except last for features
                train_array[:, -1],   # Last column as target
                test_array[:, :-1],   # Same for test data
                test_array[:, -1]
            )

            # Model Definitions
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            # Hyperparameter Grid for Model Tuning
            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 
                                 'absolute_error', 'poisson'],
                    # Additional parameters commented out for potential future use
                    # 'splitter': ['best','random'],
                    # 'max_features': ['sqrt','log2'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                    # Additional parameters available for extension:
                    # 'criterion': ['squared_error', 'friedman_mse', 
                    #              'absolute_error', 'poisson'],
                    # 'max_features': ['sqrt','log2', None],
                },
                "Gradient Boosting": {
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                    # Additional parameters available:
                    # 'loss': ['squared_error', 'huber', 'absolute_error', 'quantile'],
                    # 'criterion': ['squared_error', 'friedman_mse'],
                    # 'max_features': ['auto','sqrt','log2'],
                },
                "Linear Regression": {},  # No hyperparameters for basic linear regression
                "XGBRegressor": {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "CatBoosting Regressor": {
                    'depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor": {
                    'learning_rate': [.1, .01, 0.5, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                    # 'loss': ['linear','square','exponential'],
                }
            }

            # Model Evaluation
            logging.info("Evaluating models with hyperparameter tuning")
            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params
            )

            # Determine Best Model
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            # Quality Check
            if best_model_score < 0.6:
                raise CustomException("No suitable model found (R² < 0.6)")
            logging.info(f"Best model identified: {best_model_name}")

            # Model Persistence
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            logging.info(f"Saved best model to {self.model_trainer_config.trained_model_file_path}")

            # Final Evaluation
            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            logging.info(f"Best model R² score: {r2_square}")

            return r2_square

        except Exception as e:
            # Error handling and logging
            logging.error("Error occurred during model training", exc_info=True)
            raise CustomException(e, sys)