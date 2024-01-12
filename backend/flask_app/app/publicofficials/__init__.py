from flask import Blueprint

bp = Blueprint('publicofficials', __name__)

from app.publicofficials import routes