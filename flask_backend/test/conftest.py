import pytest

from app import create_app
from app.logic.mongo.database import get_user_collection, get_po_collection, get_generated_post_collection, get_token_blocklist
from test.auth_actions import AuthActions


@pytest.fixture()
def app():
    app  = create_app()
    
    #reset database
    get_user_collection().delete_many({})
    get_po_collection().delete_many({})
    get_generated_post_collection().delete_many({})
    get_token_blocklist().delete_many({})

    yield app

@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture()
def client(app):
    return app.test_client()