#how to handle things and transformation
import sys, os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer #use to create a pipeline for features
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.logger import logging
from src.exception import CustomException
from src.utils import save_obj

@dataclass

class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifact","preprocessor.pkl")



class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    
    def get_data_transformer_object(self): #contains features
        '''
            this function is resonsible for the data transformation        
        '''

        try:
            num_cols = ['writing_score','reading_score']
            cat_cols = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course',
            ]
            #we have some missing values so we need to handle that also

            logging.info('numerical scaling start')

            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ("scaler",StandardScaler())
                ]

            
            )

            logging.info('numerical scaling done')


            logging.info('categorical encoding start')

            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False)),
                ]
            )

            logging.info('categorical encoding done')

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline, num_cols),
                    ('cat_pipline',cat_pipeline, cat_cols)       

                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException (e,sys)
        


    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)


            logging.info('reading train and test data completed')
            logging.info('obtaining preprocessing object')

            preprocessing_obj = self.get_data_transformer_object()

            target_col = "math_score"
            num_col = ['writing_score','reading_score']

            input_feature_train_df = train_df.drop(columns=[target_col], axis = 1)
            target_feature_train_df = train_df[target_col]
            
            input_feature_test_df = test_df.drop(columns=[target_col], axis = 1)
            target_feature_test_df = test_df[target_col]

            logging.info(
                'applying processing object on training and test data'
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df, )
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            #A short technique for concatenation of arrays using numpy
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]


            logging.info('saving the preprocessing object')

            save_obj(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException (e,sys)