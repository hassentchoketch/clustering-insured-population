import os 
import sys
import logging

# format for logging
logging_str ="[%(asctime)s: %(levelname)s: %(module)s: %(message)s]" 

# create a directory for logs if it doesn't exist
log_dir = "logs"
log_filepath = os.path.join(log_dir,"runnig_logs.log")
os.makedirs(log_dir,exist_ok=True)

# set up logging to file and console
logging.basicConfig(
    level=logging.INFO, 
    format=logging_str,
    handlers=[
            logging.FileHandler(log_filepath),
            logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger('insuredSegmeterLogger')


