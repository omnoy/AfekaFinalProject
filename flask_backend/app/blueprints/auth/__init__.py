from flask import Blueprint
from app.logic.mongo.token_blocklist_data_manager_mongodb import TokenBlocklistDataManagerMongoDB
from app.logic.mongo.user_data_manager_mongodb import UserDataManagerMongoDB

bp = Blueprint('auth', __name__)
user_service = UserDataManagerMongoDB()
token_blocklist_service = TokenBlocklistDataManagerMongoDB()

from app.blueprints.auth import routes