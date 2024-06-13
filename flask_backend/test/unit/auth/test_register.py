from app.models.user import User
from app.logic.mongo.database import get_user_collection
import json

def test_create_user(client):
    # Test case: Create a user with valid data
    user_dict = {"username": "testman", "password": "test", "email": "test@test.com", "position": "test master", "role": 'basic_user'}
    test_user = User(**user_dict)
    response = client.post("/auth/register", json=user_dict)
    
    assert response.status_code == 200

    response_user_dict = json.loads(json.loads(response.data)['user'])
    assert all(user_item in response_user_dict.items() for user_item in response_user_dict.items() if user_item[0] != 'password')
    
    db_user_dict = get_user_collection().find_one({"email":"test@test.com"})

    assert all(user_item in db_user_dict.items() for user_item in user_dict.items() if user_item[0] != 'password')

def test_create_user_invalid_email(client):
    # Test case: Attempt to create a user with an invalid email
    user_dict = {"username": "testman", "password": "test", "email": "invalidemailaddress", "position": "test master", "role": 'basic_user'}
    response = client.post("/auth/register", json=user_dict)

    assert response.status_code == 400 

def test_create_user_missing_field(client):
    # Test case: Attempt to create a user with a missing field
    user_dict = {"username": "testman", "password": "test", "position": "test master", "role": 'basic_user'}
    response = client.post("/auth/register", json=user_dict)

    assert response.status_code == 400

def test_create_user_existing_email(client, auth):
    # Test case: Attempt to create a user with an existing email
    existing_email = "existing@test.com"
    auth.create(email=existing_email)
    user_dict = {"username": "newuser", "password": "newpassword", "email": existing_email, "position": "test position", "role": 'basic_user'}
    response = client.post("/auth/register", json=user_dict)
    assert response.status_code == 400  # Bad Request

def test_create_user_invalid_role(client):
    # Test case: Attempt to create a user with an invalid role
    invalid_role = "invalid_role"
    user_dict = {"username": "testman", "password": "test", "email": "test@test.com", "position": "test master", "role": invalid_role}
    response = client.post("/auth/register", json=user_dict)
    assert response.status_code == 400  # Bad Request

def test_create_user_missing_username(client):
    # Test case: Attempt to create a user without providing a username
    user_dict = {"password": "test", "email": "test@test.com", "position": "test master", "role": 'basic_user'}
    response = client.post("/auth/register", json=user_dict)
    assert response.status_code == 400  # Bad Request

def test_create_user_empty_fields(client):
    # Test case: Attempt to create a user with empty fields
    user_dict = {"username": "", "password": "", "email": "", "position": "", "role": ''}
    response = client.post("/auth/register", json=user_dict)
    assert response.status_code == 400  # Bad Request
