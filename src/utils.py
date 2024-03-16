#it will have all the common things that could come
import os, sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
import dill 

def save_obj(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)