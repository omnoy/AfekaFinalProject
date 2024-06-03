from flask import Blueprint
from app.logic.mongo.user_data_manager_mongodb import userDataManagerMongoDB

bp = Blueprint('users', __name__)
user_service = userDataManagerMongoDB

from app.blueprints.users import routes