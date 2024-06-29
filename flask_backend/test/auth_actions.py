from app.logic.mongo.database import get_user_collection
from app.models.user import User

class AuthActions():
    def __init__(self, client):
        self.client = client

    def create_admin_user(self, username="admin", password='admin123', email="admin@test.com"):
        user_data = {"username": username, "password": password, "email": email, "position": "admin", "role": "admin_user"}
        user = User(**user_data)
        inserted_obj = get_user_collection().insert_one(user.model_dump(exclude={'id'}))
        self.user_id = inserted_obj.inserted_id

        login_response = self.client.post(
            'auth/login',
            json={'email': email, 'password': password}
        )

        self.access_token = login_response.json['access_token']

        result_dict = {"response": login_response, "access_token": self.access_token}

        return result_dict

    def create_basic_user(self, username='testman', password='testtest', email="test@test.com", position="tester"):
        response = self.client.post(
            'auth/register',
            json={'username':username, 'password':password, 'email':email, 'position':position}
        )
        if response.status_code != 200:
            raise Exception("Failed to create user: Email Already Exists")
        
        self.access_token = response.json['access_token']
        self.user_id = response.json['user']['id']
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
    
    def get_auth_header(self, authentication_token = None):
        if authentication_token is None:
            authentication_token = self.access_token
        return {'Authorization': 'Bearer ' + authentication_token}
    
    def get_user_id(self) -> str:
        return self.user_id

    def logout(self):
        return self.client.get('auth/logout', headers={'Authorization':self.access_token})