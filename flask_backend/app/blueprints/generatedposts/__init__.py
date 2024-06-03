from flask import Blueprint
from app.logic.mongo.generatedpost_data_manager_mongodb import generatedPostDataManagerMongo

bp = Blueprint('generatedposts', __name__)
generated_post_service = generatedPostDataManagerMongo

from app.blueprints.generatedposts import routes