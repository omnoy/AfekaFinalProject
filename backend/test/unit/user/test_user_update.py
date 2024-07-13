from app.logic.mongo.database import get_user_collection
from json import loads

from app.models.user import User

def test_update_username(client, auth):
    # Test updating the username of a user
    email = "test@test.com"

    new_username = "newname"

    user_data = {"username": "testman", "password": "testtest", "email": email, "position": "tester"}

    auth.create_basic_user(**user_data)

    user_update_data = {"username": new_username}

    response = client.put("/user/update", json=user_update_data, headers=auth.get_auth_header())
    
    assert response.status_code == 200

    assert response.json['user']['username'] == new_username

    db_user_dict = get_user_collection().find_one({"email":email})

    assert db_user_dict['username'] == new_username

def test_update_position(client, auth):
    # Test updating the position of a user
    email = "test@test.com"
    new_position = "newposition"

    user_data = {"username": "testman", "password": "testtest", "email": "test@test.com", "position": "tester"}
    auth.create_basic_user(**user_data)

    user_update_data = {"position": new_position}
    
    response = client.put("/user/update", json=user_update_data, headers=auth.get_auth_header())

    assert response.status_code == 200
    assert response.json['user']['position'] == new_position
    db_user_dict = get_user_collection().find_one({"email": email})

    assert db_user_dict['position'] == new_position

def test_update_user_with_same_data(client, auth):
    # Test updating a user with the same data
    user_data = {"username": "testman", "password": "testtest", "email": "test@test.com", "position": "tester"}
    auth.create_basic_user(**user_data)
    
    user_data.pop("password")
    
    response = client.put("/user/update", json=user_data, headers=auth.get_auth_header())

    assert response.status_code == 200

def test_update_user_invalid_fields(client, auth):
    # Test updating a user with missing fields
    email = "test@test.com"
    user_data = {"username": "testman", "password": "testtest", "email": "test@test.com", "position": "tester"}
    auth.create_basic_user(**user_data)
    user_update_data = {"address": "1234 Main St."}
    
    response = client.put("/user/update", json=user_update_data, headers=auth.get_auth_header())

    assert response.status_code == 400

def test_update_user_invalid_username(client, auth):
    # Test updating a user with an invalid username
    user_data = {"username": "testman", "password": "testtest", "email": "test@test.com", "position": "tester"}
    auth.create_basic_user(**user_data)
    
    invalid_username_list = ["", "a", "ab", "abc", "אבגד", " "]
    for username in invalid_username_list:
        user_update_data = {"username": username}  # Username invalid
        response = client.put("/user/update", json=user_update_data, headers=auth.get_auth_header())
        assert response.status_code == 400

def test_update_user_invalid_position(client, auth):
    # Test updating a user with an invalid position
    user_data = {"username": "testman", "password": "testtest", "email": "test@test.com", "position": "tester"}
    auth.create_basic_user(**user_data)
    
    invalid_position_list = ["", "a", "ab", "abc", "אבגד", " "]
    for position in invalid_position_list:
        user_update_data = {"position" : position}  # Position invalid
        response = client.put("/user/update", json=user_update_data, headers=auth.get_auth_header())

        assert response.status_code == 400

def test_update_user_email_not_changeable(client, auth):
    email = "test@test.com"
    user_data = {"username": "testman", "password": "testtest", "email": email, "position": "tester"}
    auth.create_basic_user(**user_data)
    new_email = "new@test.com"
    user_update_data ={"email":new_email}
    response = client.put("/user/update", json=user_update_data, headers=auth.get_auth_header())

    assert response.status_code == 400
    db_user_dict = get_user_collection().find_one({"email": email})
    assert db_user_dict['email'] == email

def test_update_user_role_not_changeable(client, auth):
    email = "test@test.com"
    user_data = {"username": "testman", "password": "testtest", "email": email, "position": "tester"}
    auth.create_basic_user(**user_data)
    user_update_data = {"role" : "admin_user"}
    response = client.put("/user/update", json=user_data, headers=auth.get_auth_header())

    assert response.status_code == 400
    db_user_dict = get_user_collection().find_one({"email": email})
    assert db_user_dict['role'] == 'basic_user'
