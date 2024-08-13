import os
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv, find_dotenv
from app.generation_model.generation_model_wrapper import GenerationModelWrapper
from app.init_logger import initialize_logger

# dotenv extension
load_dotenv(find_dotenv())
os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY')

# logger extension
initialize_logger()

# jwt extension
jwt = JWTManager()

# generation model extension
generation_model = GenerationModelWrapper