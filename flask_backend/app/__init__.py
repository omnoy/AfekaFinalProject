from flask import Flask
from app.extensions import mongo, login_manager
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize MongoDB extension
    mongo.init_app(app)

    # Initialize LoginManager extension
    login_manager.init_app(app)

    # register blueprints
    from app.main import bp as main_bp
    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.users import bp as users_bp
    from app.blueprints.publicofficials import bp as publicofficials_bp
    from app.blueprints.generatedposts import bp as generatedposts_bp
    

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix= "/auth")
    app.register_blueprint(users_bp, url_prefix="/user")
    app.register_blueprint(publicofficials_bp, url_prefix="/publicofficial")
    app.register_blueprint(generatedposts_bp, url_prefix="/postgeneration")

    return app