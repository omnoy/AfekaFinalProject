from flask import Blueprint
from app.logic.mongo.generatedpost_data_manager_mongodb import GeneratedPostDataManagerMongoDB
from app.logic.mongo.publicofficial_data_manager_mongodb import PublicOfficialDataManagerMongoDB
bp = Blueprint('generatedposts', __name__)

generated_post_service = GeneratedPostDataManagerMongoDB()
public_offical_service = PublicOfficialDataManagerMongoDB()

from app.blueprints.generatedposts import routes