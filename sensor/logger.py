import logging
import os
from datetime import datetime
from from_root import from_root

LOG_FILE= f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# create logs/<log_file>.log
LOGS_PATH = os.path.join(from_root(),"logs")
os.makedirs(LOGS_PATH, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE)

logging.basicConfig(
                    filename=LOG_FILE_PATH,
                    format="[%(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
                    level = logging.INFO
                )

