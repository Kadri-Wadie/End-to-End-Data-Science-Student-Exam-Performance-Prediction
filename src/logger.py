import logging
import os
from datetime import datetime

# Log filename: m_Day_Year_Hour_Minute_Second.log (e.g., m_05_2023_14_30_00.log)
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Directory path: "logs" folder in the current working directory
logs_path = os.path.join(os.getcwd(), "logs",LOG_FILE)
os.makedirs(logs_path, exist_ok=True)  # Create directory if it doesn’t exist

# Full path to the log file (e.g., ./logs/m_05_2023_14_30_00.log)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

if __name__=="__main__":
    logging.info("Logging has started")
