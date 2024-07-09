from app.logic.mongo.database import get_user_collection
from bson import ObjectId

def test_add_favorite_public_official(client, auth, public_official_actions):
    # Test adding public official to favorites
    public_official_id = public_official_actions.create_public_official().get_id()
    
    auth.create_basic_user()

    response = client.put(f'user/favorites/public_official/{public_official_id}', headers=auth.get_auth_header())

    assert response.status_code == 200

    user = auth.login()['response'].json['user']
    
    assert public_official_id in user['favorites']['public_official']
    
    user = get_user_collection().find_one({"_id": ObjectId(auth.get_user_id())})
    
    assert public_official_id in user['favorites']['public_official']
    

def test_add_favorite_generated_post(client, auth, public_official_actions, generated_post_actions):
    # Test adding generated post to favorites
    public_official_id = public_official_actions.create_public_official().get_id()
    
    auth.create_basic_user()

    generated_post_actions.create_generated_post(user_id=auth.get_user_id(), public_official_id=public_official_id)

    generated_post_id = generated_post_actions.get_generated_post_id()
    
    response = client.put(f'user/favorites/generated_post/{generated_post_id}', headers=auth.get_auth_header())

    assert response.status_code == 200

    user = auth.login()['response'].json['user']
    
    assert generated_post_id in user['favorites']['generated_post']
    
    user = get_user_collection().find_one({"_id": ObjectId(auth.get_user_id())})
    
    assert generated_post_id in user['favorites']['generated_post']

def test_add_invalid_favorite_type(client, auth):
    # Test adding invalid favorite type
    auth.create_basic_user()

    response = client.put(f'user/favorites/invalid/667197af047f22ff2e4054bd', headers=auth.get_auth_header())

    assert response.status_code == 404 # Not Found

def test_add_favorite_public_official_invalid_id(client, auth):
    # Test adding public official to favorites with an invalid id
    auth.create_basic_user()

    response = client.put(f'user/favorites/public_official/667197af047f22ff2e4054bd', headers=auth.get_auth_header())

    assert response.status_code == 404 # Not Found

def test_add_favorite_generated_post_invalid_id(client, auth):
    # Test adding public official to favorites with an invalid id
    auth.create_basic_user()

    response = client.put(f'user/favorites/generated_post/667197af047f22ff2e4054bd', headers=auth.get_auth_header())

    assert response.status_code == 404 # Not Found

def test_add_favorite_generated_post_unauthorized(client, auth, public_official_actions, generated_post_actions):
    # Test adding a generated post of another user to favorites
    public_official_id = public_official_actions.create_public_official().get_id()
    
    auth.create_basic_user()

    generated_post_actions.create_generated_post(user_id=auth.get_user_id(), public_official_id=public_official_id)

    generated_post_id = generated_post_actions.get_generated_post_id()
    
    auth.create_basic_user(email="test2@gmail.com")
    
    response = client.put(f'user/favorites/generated_post/{generated_post_id}', headers=auth.get_auth_header())

    assert response.status_code == 403
