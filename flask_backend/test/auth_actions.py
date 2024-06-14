from app.logic.mongo.database import get_user_collection
from app.models.user import User

class AuthActions():
    def __init__(self, client):
        self.client = client

    def create_admin(self, username='admin', password='admin123', email="admin@test.com"):
        user_data = {"username": username, "password": password, "email": email, "position": "admin", 'role': 'admin'}
        user = User(**user_data)
        get_user_collection().insert_one(user.model_dump(exclude={'id'}))
        login_response = self.client.post(
            'auth/login',
            json={'email': email, 'password': password}
        )

        self.access_token = 'Bearer ' + login_response.json['access_token']

        result_dict = {"response": login_response, "access_token": self.access_token}

        return result_dict

    def create(self, username='testman', password='testtest', email="test@test.com", position="tester"):
        response = self.client.post(
            'auth/register',
            json={'username':username, 'password':password, 'email':email, 'position':position}
        )

        self.access_token = 'Bearer ' +  response.json['access_token']
        
        result_dict = {"response": response, "access_token": self.access_token}

        return result_dict

    def login(self, email='test@test.com', password='testtest'):
        result = self.client.post(
            'auth/login',
            json={'email': email, 'password': password}
        )
        self.access_token = result.json['access_token']

        result_dict= {"response": result, "access_token": self.access_token}

        return result_dict

    def logout(self):
        return self.client.get('auth/logout', headers={'Authorization':self.access_token})