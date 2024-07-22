from flask import Blueprint
from app.logic.mongo.user_data_manager_mongodb import UserDataManagerMongoDB
from app.logic.mongo.publicofficial_data_manager_mongodb import PublicOfficialDataManagerMongoDB
from app.logic.mongo.generatedpost_data_manager_mongodb import GeneratedPostDataManagerMongoDB

bp = Blueprint('users', __name__)
user_service = UserDataManagerMongoDB()
public_official_service = PublicOfficialDataManagerMongoDB()
generated_post_service = GeneratedPostDataManagerMongoDB()

from app.blueprints.users import routes