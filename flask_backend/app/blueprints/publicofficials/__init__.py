from flask import Blueprint
from app.logic.mongo.publicofficial_data_manager_mongodb import publicOfficialDataManagerMongo

bp = Blueprint('publicofficials', __name__)
public_official_service = publicOfficialDataManagerMongo

from app.blueprints.publicofficials import routes