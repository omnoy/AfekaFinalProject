from app.models.user import User
from app.models.user_role import UserRole
from app.logic_mongo.user_data_manager_mongodb import UserDataManagerMongoDB
import json

def test_create_user(client):
    user_dict = {"username": "testman", "password": "test", "personal_name": "test", "email": "test@test.com", "role": 'basic_user'}
    test_user = User(**user_dict)
    response = client.post("/register", content_type='application/json', data=json.dumps(user_dict))
    response_user_dict = json.loads(response.data)['user']
    response_user = User(**response_user_dict)
    print(response.status)
    assert response.status_code == 200 and \
        all(response_item==test_item for response_item, test_item in zip(response_user.__dict__.items(), test_user.__dict__.items()) if response_item[0] != 'id')
    
    db_user = UserDataManagerMongoDB().get_user_by_email('test@test.com')

    assert all(response_item==db_item for response_item, db_item in zip(response_user.__dict__.items(), db_user.__dict__.items()))

    
def test_login_user(client):
    user_dict = {"username": "testman", "password": "test", "personal_name": "test", "email": "test@test.com", "role": 'basic_user'}
    test_user = User(**user_dict)
    UserDataManagerMongoDB().create_user(test_user)

    response = client.post("/login", data={"username": "testman", "password": "teest"})
    assert response.status_code == 200