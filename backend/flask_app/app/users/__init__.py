from flask import Blueprint
from app.logic_mongo.user_data_manager_mongodb import UserDataManagerMongoDB

bp = Blueprint('users', __name__)
user_service = UserDataManagerMongoDB()

from app.users import routes