from flask import render_template
from app.main import bp
from app.extensions import mongo

@bp.route('/')
def home():
    return render_template("home.html")