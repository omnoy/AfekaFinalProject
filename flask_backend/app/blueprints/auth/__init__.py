from flask import Blueprint
from app.logic.mongo.user_data_manager_mongodb import UserDataManagerMongoDB

bp = Blueprint('auth', __name__)
user_service = UserDataManagerMongoDB()

from app.blueprints.auth import routes