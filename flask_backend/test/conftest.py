import pytest

from app import create_app
from app.logic.mongo.user_data_manager_mongodb import UserDataManagerMongoDB
from app.logic.mongo.publicofficial_data_manager_mongodb import PublicOfficialDataManagerMongoDB
from app.logic.mongo.generatedpost_data_manager_mongodb import GeneratedPostDataManagerMongoDB

def pytest_configure():
    pytest.user_dm = UserDataManagerMongoDB()
    pytest.po_dm = PublicOfficialDataManagerMongoDB()
    pytest.gp_dm = GeneratedPostDataManagerMongoDB()

@pytest.fixture()
def app():
    app  = create_app()
    with app.app_context():
        pytest.user_dm.delete_all_users()
        pytest.po_dm.delete_all_public_officials()
        pytest.gp_dm.delete_all_generated_posts()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()