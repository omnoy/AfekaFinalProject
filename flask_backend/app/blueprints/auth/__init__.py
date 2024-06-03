from flask import Blueprint
from app.logic.mongo.user_data_manager_mongodb import userDataManagerMongoDB

bp = Blueprint('auth', __name__)
user_service = userDataManagerMongoDB

from app.blueprints.auth import routes