from app.models.user import User
from app.logic.mongo.database import get_user_collection
import json

user_dict_template = {"username": "testman", "password": "testtest", "email": "test@test.com"}

def test_register_user(client):
    # Test case: register a user with valid data
    user_dict = user_dict_template.copy()
    
    response = client.post("/auth/register", json=user_dict)
    
    assert response.status_code == 200

    response_user_dict = response.json['user']
    assert all(user_item in response_user_dict.items() for user_item in user_dict.items() if user_item[0] != 'password')
    
    db_user_dict = get_user_collection().find_one({"email":"test@test.com"})
    assert all(user_item in db_user_dict.items() for user_item in user_dict.items() if user_item[0] != 'password')

def test_register_user_invalid_email(client):
    # Test case: Attempt to register a user with an invalid email
    user_dict = user_dict_template.copy()
    for invalid_emails in ["invalidemail", "invalidemail@", "invalidemail@com", "invalidemail.com"]:
        user_dict["email"] = invalid_emails
        response = client.post("/auth/register", json=user_dict)
        assert response.status_code == 400
        
def test_register_user_invalid_password(client):
    # Test case: Attempt to register a user with an invalid password
    user_dict = user_dict_template.copy()
    for invalid_password in ["לאתקין", "short", ""]:
        user_dict["password"] = invalid_password
        response = client.post("/auth/register", json=user_dict)
        assert response.status_code == 400

def test_register_user_invalid_username(client):
    # Test case: Attempt to register a user with an invalid username
    user_dict = user_dict_template.copy()
    for invalid_username in ["", "a", "ab", "abc", "אבגד", " "]:
        user_dict["username"] = invalid_username
        response = client.post("/auth/register", json=user_dict)
        assert response.status_code == 400

def test_register_user_admin_role(client):
    # Test case: Attempt to register a user with an admin role
    user_dict = user_dict_template.copy()
    
    user_dict["role"] = "admin_user"
    response = client.post("/auth/register", json=user_dict)

    assert response.status_code == 403 # Forbidden

def test_register_user_missing_field(client):
    # Test case: Attempt to register a user with a missing username, email address or password
    for field in ["username", "email", "password"]:
        user_dict = user_dict_template.copy()
        user_dict.pop(field)
        response = client.post("/auth/register", json=user_dict)
        assert response.status_code == 400

def test_register_user_existing_email(client, auth):
    # Test case: Attempt to register a user with an existing email
    existing_email = "existing@test.com"
    auth.create_basic_user(email=existing_email)
    
    user_dict = user_dict_template.copy()
    user_dict["email"] = existing_email
    response = client.post("/auth/register", json=user_dict)
    assert response.status_code == 409  # Conflict
