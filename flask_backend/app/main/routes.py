from flask import render_template
from app.main import bp
from app.extensions import mongo

@bp.route('/test')
def index():
    user = mongo.db.users.find_one({"username": "testman123"})
    return f'This is The Blueprint Mr. {user['username']}'

