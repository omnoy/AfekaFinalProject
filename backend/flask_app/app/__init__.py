from flask import Flask
from app.extensions import mongo
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize MongoDB extension
    mongo.init_app(app)
    
    # register blueprints
    from app.main import bp as main_bp
    from app.users import bp as users_bp
    from app.publicofficials import bp as publicofficials_bp
    from app.generatedposts import bp as generatedposts_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(publicofficials_bp)
    app.register_blueprint(generatedposts_bp)

    return app