from bson import ObjectId
from app.logic.mongo.database import get_user_collection


def test_removing_favorite_public_official(client, auth, public_official_actions):
    # Test removing a public official from favorites
    public_official_id = public_official_actions.create_public_official().get_id()
    
    auth.create_basic_user()

    client.put(f'user/favorites/public_official/{public_official_id}', headers=auth.get_auth_header())

    response = client.delete(f'user/favorites/public_official/{public_official_id}', headers=auth.get_auth_header())

    assert response.status_code == 200
    
    user = get_user_collection().find_one({"_id": ObjectId(auth.get_user_id())})
    
    assert public_official_id not in user['favorites']['public_official']
    
    

def test_remove_favorite_generated_post(client, auth, public_official_actions, generated_post_actions):
    # Test removing generated post from favorites
    
    auth.create_basic_user()
    
    user_id = auth.get_user_id()

    public_official_id = public_official_actions.create_public_official().get_id()
    
    generated_post_id = generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id).get_id()

    response = client.put(f'user/favorites/generated_post/{generated_post_id}', headers=auth.get_auth_header())

    response = client.delete(f'user/favorites/generated_post/{generated_post_id}', headers=auth.get_auth_header())

    assert response.status_code == 200

    user = get_user_collection().find_one({"_id": ObjectId(auth.get_user_id())})
    
    assert public_official_id not in user['favorites']['generated_post']

def test_remove_favorite_public_official_id_not_in_favorites(client, auth, public_official_actions):
    # Test removing public official to favorites with an invalid id
    auth.create_basic_user()

    public_official_id = public_official_actions.create_public_official().get_id()

    response = client.delete(f'user/favorites/public_official/{public_official_id}', headers=auth.get_auth_header())

    assert response.status_code == 404 # Not Found

def test_remove_favorite_generated_post_id_not_in_favorites(client, auth, public_official_actions, generated_post_actions):
    # Test removing public official to favorites with an invalid id
    auth.create_basic_user()

    user_id = auth.get_user_id()

    public_official_id = public_official_actions.create_public_official().get_id()
    
    generated_post_id = generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id).get_id()

    response = client.delete(f'user/favorites/generated_post/{generated_post_id}', headers=auth.get_auth_header())

    assert response.status_code == 404 # Not Found
    
def test_delete_invalid_favorite_type(client, auth):
    # Test deleting invalid favorite type
    auth.create_basic_user()

    response = client.delete(f'user/favorites/invalid/667197af047f22ff2e4054bd', headers=auth.get_auth_header())

    assert response.status_code == 404 # Not Found