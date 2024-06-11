from flask import Blueprint
from app.logic.mongo.publicofficial_data_manager_mongodb import PublicOfficialDataManagerMongoDB

bp = Blueprint('publicofficials', __name__)

public_official_service = PublicOfficialDataManagerMongoDB()

from app.blueprints.publicofficials import routes