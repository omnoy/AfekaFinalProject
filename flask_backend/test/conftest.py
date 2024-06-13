import pytest

from app import create_app
from app.logic.mongo.database import get_user_collection, get_po_collection, get_generated_post_collection, get_token_blocklist
from app.models.user import User

@pytest.fixture()
def app():
    app  = create_app()
    
    #reset database
    get_user_collection().delete_many({})
    get_po_collection().delete_many({})
    get_generated_post_collection().delete_many({})
    get_token_blocklist().delete_many({})

    yield app

class AuthActions():
    def __init__(self, client):
        self.client = client

    def create(self, username='testman', password='test', email="test@test.com", position="tester", role='basic_user'):
        result = self.client.post(
            'auth/register',
            json={'username':username, 'password':password, 'email':email, 'position':position, 'role':role}
        )

        self.access_token = result.json['access_token']

        return result

    def login(self, email='test@test.com', password='test'):
        result = self.client.post(
            'auth/login',
            json={'email': email, 'password': password}
        )
        self.access_token = result.json['tokens']['access']
        return result
        

    def logout(self):
        return self.client.get('auth/logout', headers={'Authorization':self.access_token})

@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture()
def client(app):
    return app.test_client()