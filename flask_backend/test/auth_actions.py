
import pytest
from app.models.user import User
from app.logic_mongo.user_data_manager_mongodb import UserDataManagerMongoDB
class AuthActions():
    def __init__(self, client, username='TestUser', password='TestPass'):
        self.client = client
        self.username = username
        self.password = password

    def create(self):
        with self.client.application.app_context():
            test_user = User(username=self.username, password=self.password, personal_name="test", email="test@test.com", role='basic_user')
            UserDataManagerMongoDB.create_user(test_user)

    def login(self):
        return self.client.post(
            '/login',
            data={'username': self.username, 'password': self.password}
        )

    def logout(self):
        return self.client.get('/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)