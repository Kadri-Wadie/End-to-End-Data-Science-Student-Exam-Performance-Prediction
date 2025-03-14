import logging
import os
from datetime import datetime

# Generate timestamped log filename format: Month_Day_Year_Hour_Minute_Second.log
# Example: '05_15_2023_14_30_00.log' (May 15th, 2023 at 2:30:00 PM)
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create log directory path structure:
# - Base directory: Current working directory
# - Subdirectory: 'logs' folder
# - Sub-subdirectory: Individual log file folder (named same as LOG_FILE)
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
# Create nested directory structure if it doesn't exist
# Note: This creates a new folder for each log file (uncommon practice)
os.makedirs(logs_path, exist_ok=True)

# Create full path to log file within its dedicated subdirectory
# Final path structure: ./logs/MM_DD_YYYY_HH_MM_SS.log/MM_DD_YYYY_HH_MM_SS.log
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure Python's logging system
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Full path to log file
    format=(
        "[%(asctime)s] %(lineno)d %(name)s - "  # Timestamp, line number, logger name
        "%(levelname)s - %(message)s"           # Log level and message
    ),
    level=logging.INFO  # Capture all logs at INFO level and above
)

# Test logger when file is executed directly
if __name__ == "__main__":
    logging.info("Logging system initialized successfully")
    logging.warning("This is a test warning message")