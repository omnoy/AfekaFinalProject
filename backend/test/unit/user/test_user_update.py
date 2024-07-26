from app.logic.mongo.database import get_user_collection
from json import loads

from app.models.user import User

user_dict_template = {"username": "testman", "password": "testtest", "email": "test@test.com"}

def test_update_username(client, auth):
    # Test updating the username of a user

    new_username = "newname"

    auth.create_basic_user(**user_dict_template)

    user_update_data = {"username": new_username}

    response = client.put("/user/update", json=user_update_data, headers=auth.get_auth_header())
    
    assert response.status_code == 200

    assert response.json['user']['username'] == new_username

    db_user_dict = get_user_collection().find_one({"email": user_dict_template['email']})

    assert db_user_dict['username'] == new_username

def test_update_user_with_same_data(client, auth):
    # Test updating a user with the same data
    
    user_dict = auth.create_basic_user(**user_dict_template)["response"].json['user']
    
    response = client.put("/user/update", json=user_dict, headers=auth.get_auth_header())

    assert response.status_code == 200
    
    db_user_dict = get_user_collection().find_one({"email": user_dict_template['email']})
    db_user_dict['id'] = str(db_user_dict['_id'])
    db_user_dict.pop('_id')
    db_user_dict.pop('password')
    
    assert db_user_dict == user_dict
    

def test_update_user_invalid_fields(client, auth):
    # Test updating a user with invalid fields
    auth.create_basic_user(**user_dict_template)
    user_update_data = {"address": "1234 Main St."}
    
    response = client.put("/user/update", json=user_update_data, headers=auth.get_auth_header())

    assert response.status_code == 400

def test_update_user_invalid_username(client, auth):
    # Test updating a user with an invalid username
    auth.create_basic_user(**user_dict_template)
    
    for username in ["", "a", "ab", "abc", "אבגד", "אאאאאא", " "]:
        user_update_data = {"username": username}  # Username invalid
        response = client.put("/user/update", json=user_update_data, headers=auth.get_auth_header())
        assert response.status_code == 400

def test_update_user_email_not_changeable(client, auth):
    auth.create_basic_user(**user_dict_template)
    new_email = "new@test.com"
    user_update_data ={"email":new_email}
    response = client.put("/user/update", json=user_update_data, headers=auth.get_auth_header())

    assert response.status_code == 400
    db_user_dict = get_user_collection().find_one({"email": user_dict_template['email']})
    assert db_user_dict['email'] == user_dict_template['email']

def test_update_user_role_not_changeable(client, auth):
    auth.create_basic_user(**user_dict_template)
    user_update_data = {"role" : "admin_user"}
    response = client.put("/user/update", json=user_update_data, headers=auth.get_auth_header())

    assert response.status_code == 400
    db_user_dict = get_user_collection().find_one({"email": user_dict_template['email']})
    assert db_user_dict['role'] == 'basic_user'
