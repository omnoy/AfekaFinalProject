from flask import Blueprint
from app.logic_mongo.generatedpost_data_manager_mongodb import GeneratedPostDataManagerMongoDB
bp = Blueprint('generatedposts', __name__)
generated_post_service = GeneratedPostDataManagerMongoDB()

from app.generatedposts import routes