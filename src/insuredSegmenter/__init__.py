import os 
import sys
import logging

logging_str ="[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir,"runnig_logs.log")
os.makedirs(log_dir,exist_ok=True)

logging.basicConfig(
    filename=log_dir, 
    level=logging.INFO, 
    format=logging_str,
    handlers=[logging.FileHandler(filename=log_filepath),
            logging.StreamHandler(sys.stdout)]
)

logging.info("Logging has been set up.")
