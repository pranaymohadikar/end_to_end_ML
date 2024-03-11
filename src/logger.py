import logging
import os, sys
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y__%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE) #create a folder and all the log file will be getting generated there
os.makedirs(logs_path, exist_ok=True)


LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG,
)


if __name__ == "__main__":
    logging.info('logging has started')