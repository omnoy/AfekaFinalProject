import pytest

from app import create_app
from app.logic.mongo.database import get_user_collection, get_public_official_collection, get_generated_post_collection, get_token_blocklist
from test.actions.generated_post_actions import GeneratedPostActions
from test.actions.public_official_actions import PublicOfficialActions
from test.actions.auth_actions import AuthActions


@pytest.fixture()
def app():
    app  = create_app()
    app.config.update({
        "MONGO_URI": "mongodb://localhost:27017/statementGenDBTest",
        "TESTING": True,
    })
    
    #reset database
    get_user_collection().delete_many({})
    get_public_official_collection().delete_many({})
    get_generated_post_collection().delete_many({})
    get_token_blocklist().delete_many({})

    yield app

@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def public_official_actions(client):
    return PublicOfficialActions(client)

@pytest.fixture
def generated_post_actions(client):
    return GeneratedPostActions(client)

@pytest.fixture()
def client(app):
    return app.test_client()