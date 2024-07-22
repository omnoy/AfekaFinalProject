import logging
import traceback
import sys

# log uncaught exceptions
def log_exceptions(type, value, tb):
    for line in traceback.TracebackException(type, value, tb).format(chain=True):
        logging.exception(line)
    logging.exception(value)

    sys.__excepthook__(type, value, tb)

# initialize logger
def initialize_logger():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='postGenerator.log', encoding='utf-8', level=logging.DEBUG)
    
    sys.excepthook = log_exceptions