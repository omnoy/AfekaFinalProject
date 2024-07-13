from app.models.user import User
from app.logic.mongo.database import get_user_collection
import json

def test_register_user(client):
    # Test case: register a user with valid data
    user_dict = {"username": "testman", "password": "testtest", "email": "test@test.com", "position": "test master"}
    response = client.post("/auth/register", json=user_dict)
    
    assert response.status_code == 200

    response_user_dict = response.json['user']
    assert all(user_item in response_user_dict.items() for user_item in user_dict.items() if user_item[0] != 'password')
    
    db_user_dict = get_user_collection().find_one({"email":"test@test.com"})
    assert all(user_item in db_user_dict.items() for user_item in user_dict.items() if user_item[0] != 'password')

def test_register_user_invalid_email(client):
    # Test case: Attempt to register a user with an invalid email
    user_dict = {"username": "testman", "password": "testtest", "email": "invalidemailaddress", "position": "test master"}
    response = client.post("/auth/register", json=user_dict)

    assert response.status_code == 400 

def test_register_user_admin_role(client):
    # Test case: Attempt to register a user with an admin role
    user_dict = {"username": "testman", "password": "testtest", "email": "invalidemailaddress", "position": "test master", "role": "admin_user"}
    response = client.post("/auth/register", json=user_dict)

    assert response.status_code == 403 # Forbidden

def test_register_user_missing_field(client):
    # Test case: Attempt to register a user with a missing username, email address or password
    user_dict = {"username": "testman", "password": "testtest", "position": "test master"}
    response = client.post("/auth/register", json=user_dict)

    assert response.status_code == 400

def test_register_user_existing_email(client, auth):
    # Test case: Attempt to register a user with an existing email
    existing_email = "existing@test.com"
    auth.create_basic_user(email=existing_email)
    user_dict = {"username": "newuser", "password": "newpassword", "email": existing_email, "position": "test position"}
    response = client.post("/auth/register", json=user_dict)
    assert response.status_code == 409  # Conflict
