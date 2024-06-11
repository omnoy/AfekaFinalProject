import pytest

from app.models.user import User
from app.models.user_role import UserRole
import json

def test_create_user(client):
    user_dict = {"username": "testman", "password": "test", "email": "test@test.com", "position": "test master", "role": 'basic_user'}
    test_user = User(**user_dict)
    response = client.post("/auth/register", json=user_dict)
    
    assert response.status_code == 200

    response_user_dict = json.loads(json.loads(response.data)['user'])
    assert all(user_item in response_user_dict.items() for user_item in response_user_dict.items() if user_item[0] != 'password')
    
    db_user = pytest.user_dm.get_user_by_email('test@test.com')

    assert all(user_item in db_user.__dict__.items() for user_item in user_dict.items() if user_item[0] != 'password')

    
def test_login_user(client):
    user_dict = {"username": "testman", "password": "test", "email": "test@test.com", "position": "test master", "role": 'basic_user'}
    test_user = User(**user_dict)
    print(test_user.password_hash)
    pytest.user_dm.create_user(test_user)

    login_info = {"email":"test@test.com", "password": "test"}
    response = client.post("/auth/login", json=login_info)
    assert response.status_code == 200

def test_create_user_invalid_email(client):
    user_dict = {"username": "testman", "password": "test", "email": "invalidemailaddress", "position": "test master", "role": 'basic_user'}
    response = client.post("/auth/register", json=user_dict)

    assert response.status_code == 400 

def test_create_user_missing_field(client):
    user_dict = {"username": "testman", "password": "test", "position": "test master", "role": 'basic_user'}
    response = client.post("/auth/register", json=user_dict)

    assert response.status_code == 400

def test_login_user_invalid_email(client):
    user_dict = {"username": "testman", "password": "test", "email": "test@test.com", "position": "test master", "role": 'basic_user'}
    test_user = User(**user_dict)
    pytest.user_dm.create_user(test_user)
    login_info = {"email": "invalidemailaddress", "password": "test"}
    response = client.post("/auth/login", json=login_info)

    assert response.status_code == 401

def test_login_user_invalid_password(client):
    user_dict = {"username": "testman", "password": "test", "email": "test@test.com", "position": "test master", "role": 'basic_user'}
    test_user = User(**user_dict)
    pytest.user_dm.create_user(test_user)
    login_info = {"email": "test@test.com", "password": "wrongpassword"}
    response = client.post("/auth/login", json=login_info)

    assert response.status_code == 401