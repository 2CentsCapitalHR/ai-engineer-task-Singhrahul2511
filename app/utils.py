# app/utils.py

import logging
from config import LOG_LEVEL

def setup_logger():
    """
    Configures and returns a logger for the application.
    """
    logging.basicConfig(
        level=LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

logger = setup_logger()
