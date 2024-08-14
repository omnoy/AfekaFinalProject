from flask import Flask
from flask_cors import CORS
from app.extensions import jwt
from app.config import Config
from app.logic.mongo.database import init_db
from app.config import get_config
import logging

def create_app():
    logging.info('Starting app...')
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(get_config())
    logging.info('App started')

    # Initialize MongoDB extension
    logging.info('Initializing Database...')
    init_db(app)
    logging.info('Database Initialized')

    # Initialize JWTManager extension
    logging.info('Initializing JWTManager...')
    jwt.init_app(app)
    logging.info('JWTManager Initialized')

    # register blueprints
    logging.info('Registering Blueprints...')
    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.users import bp as users_bp
    from app.blueprints.publicofficials import bp as publicofficials_bp
    from app.blueprints.generatedposts import bp as generatedposts_bp    

    app.register_blueprint(auth_bp, url_prefix= "/auth")
    app.register_blueprint(users_bp, url_prefix="/user")
    app.register_blueprint(publicofficials_bp, url_prefix="/public-official")
    app.register_blueprint(generatedposts_bp, url_prefix="/post-generation")
    logging.info('Blueprints Registered')
    
    logging.info('App started!')
    return app