from flask import Blueprint

bp = Blueprint('generatedposts', __name__)

from app.generatedposts import routes