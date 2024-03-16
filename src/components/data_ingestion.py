#reading of the data
import os, sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

#need input like where to save data, train data, test data etc

@dataclass #you will be able to define class vairable directly or wothout using __init__method
class DataIngestionConfig:
    train_data_path:str = os.path.join("artifact","train.csv")
    test_data_path:str = os.path.join("artifact","test.csv")
    raw_data_path:str = os.path.join("artifact","data.csv")

#if you have only variables then you use dataclass. if you have other functions the you can use init method
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        #now reading the data
        logging.info("entered the data ingestion method component")
        try:
            df = pd.read_csv("notebook\data\stud.csv")
            logging.info('read the dataset as DF')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index = False, header=True)

            logging.info('spplitting initiated')

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index = False, header = True)

            test_set.to_csv(self.ingestion_config.test_data_path, index = False, header = True)


            logging.info('ingestion of data completed')

            return(self.ingestion_config.train_data_path, 
                   self.ingestion_config.test_data_path, 
                   )

        except Exception as e:
            raise CustomException (e,sys)
            


if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()  #combined data ingestion


    data_transformation = DataTransformation()  #combined data transformation
    data_transformation.initiate_data_transformation(train_data, test_data)

