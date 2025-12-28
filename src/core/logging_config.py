import logging
import sys
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Create log filename with timestamp
log_filename = LOGS_DIR / f"chatbot_{datetime.now().strftime('%Y%m%d')}.log"

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create formatter
formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

# File handler - logs everything to file
file_handler = logging.FileHandler(log_filename, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Console handler - logs INFO and above to console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Create specific loggers for different components
def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module"""
    return logging.getLogger(name)

# Component loggers
api_logger = get_logger("api")
service_logger = get_logger("service")
retrieval_logger = get_logger("retrieval")
embedding_logger = get_logger("embedding")
database_logger = get_logger("database")
vector_db_logger = get_logger("vector_db")

# Log startup
root_logger.info("="*80)
root_logger.info("Chatbot logging system initialized")
root_logger.info(f"Log file: {log_filename}")
root_logger.info("="*80)
