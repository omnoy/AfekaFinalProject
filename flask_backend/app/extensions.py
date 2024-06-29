from flask_jwt_extended import JWTManager
from app.generation_model.claude_model import ClaudeModel
import logging
import traceback
import sys
import os
from dotenv import load_dotenv, find_dotenv

# dotenv extension
load_dotenv(find_dotenv())
os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY')

# logger extension
logger = logging.getLogger(__name__)
logging.basicConfig(filename='postGenerator.log', encoding='utf-8', level=logging.DEBUG)

# log uncaught exceptions
def log_exceptions(type, value, tb):
    for line in traceback.TracebackException(type, value, tb).format(chain=True):
        logging.exception(line)
    logging.exception(value)

    sys.__excepthook__(type, value, tb) # calls default excepthook

sys.excepthook = log_exceptions

# jwt extension
jwt = JWTManager()

# generation model extension
generation_model = ClaudeModel