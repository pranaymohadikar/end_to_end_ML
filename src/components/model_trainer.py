#training of code +use of different models and some metrices for evaluation

import sys, os
from dataclasses import dataclass
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from src.utils import save_obj, evaluate_model

@dataclass

class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifact", 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()


    def initiate_model_training(self, train_array, test_array):
        try:
            logging.info("splitting training and test data")
            
            X_train,y_train, X_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]

            )

            models = {
                'Random Forest': RandomForestRegressor(),
                'Decision Tree': DecisionTreeRegressor(),
                'Gradient Boosting': GradientBoostingRegressor(),
                'LinearRegression' : LinearRegression(),
                'KNeighbors': KNeighborsRegressor(),
                'XGBRegressor': XGBRegressor(),
                'CatBoost': CatBoostRegressor(),
                'AdaBoost': AdaBoostRegressor(),


            }

            model_report:dict = evaluate_model(X_train = X_train, y_train = y_train,X_test = X_test, y_test = y_test, models = models)

            #to get best model score form dict
            best_model_score = max(sorted(model_report.values()))

            #to get best model name

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException('no best model found')

            logging.info('best model found for the train and test dataset') 


            save_obj(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )   
            logging.info('shoiwng score')
            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)

            return r2_square
        except Exception as e:
            raise CustomException (e, sys)

            pass