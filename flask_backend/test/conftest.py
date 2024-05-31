import pytest

from app import create_app
from app.logic_mongo.user_data_manager_mongodb import UserDataManagerMongoDB
from app.logic_mongo.publicofficial_data_manager_mongodb import PublicOfficialDataManagerMongoDB
from app.logic_mongo.generatedpost_data_manager_mongodb import GeneratedPostDataManagerMongoDB

@pytest.fixture()
def app():
    app  = create_app()
    with app.app_context():
        UserDataManagerMongoDB().delete_all_users()
        PublicOfficialDataManagerMongoDB().delete_all_public_officials()
        GeneratedPostDataManagerMongoDB().delete_all_generated_posts()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()