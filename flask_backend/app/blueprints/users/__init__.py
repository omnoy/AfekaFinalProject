from flask import Blueprint
from app.logic.mongo.user_data_manager_mongodb import UserDataManagerMongoDB

bp = Blueprint('users', __name__)
user_service = UserDataManagerMongoDB()
from app.blueprints.users import routes