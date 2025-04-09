import logging

# Configure Logging
logging.basicConfig(
    filename="logs/jarvis.log",  # Log file path
    level=logging.INFO,  # Use DEBUG for detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Logger Object
logger = logging.getLogger()
