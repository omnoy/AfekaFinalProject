from os import getenv
from pytest_httpx import HTTPXMock
import responses

def test_get_favorite_public_official(client, auth, public_official_actions):
    # Test adding public official to favorites
    auth.create_basic_user()
    
    po_1 = public_official_actions.create_public_official()
    
    po_2 = public_official_actions.create_public_official(full_name={"eng":"Ben Gvir", "heb":"בן גביר"})
    
    po_3 = public_official_actions.create_public_official(full_name={"eng":"Bibi", "heb":"ביבי"})
    
    client.put(f'user/favorites/public_official/{po_1.get_id()}', headers=auth.get_auth_header())
    client.put(f'user/favorites/public_official/{po_2.get_id()}', headers=auth.get_auth_header())
    client.put(f'user/favorites/public_official/{po_3.get_id()}', headers=auth.get_auth_header())
    
    response = client.get(f'user/favorites/public_official', headers=auth.get_auth_header())
    
    assert response.status_code == 200
    
    for po in [po_1, po_2, po_3]:
        assert po.model_dump() in response.json['favorites']
    

def test_get_favorite_generated_post(client, auth, public_official_actions, generated_post_actions):
    # Test adding generated post to favorites
    public_official_id = public_official_actions.create_public_official().get_id()
    
    auth.create_basic_user()

    user_id = auth.get_user_id()
    
    genpost_1 = generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)
    genpost_2 = generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)
    genpost_3 = generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)

    client.put(f'user/favorites/generated_post/{genpost_1.get_id()}', headers=auth.get_auth_header())
    client.put(f'user/favorites/generated_post/{genpost_2.get_id()}', headers=auth.get_auth_header())
    client.put(f'user/favorites/generated_post/{genpost_3.get_id()}', headers=auth.get_auth_header())
    
    response = client.get(f'user/favorites/generated_post', headers=auth.get_auth_header())
    
    assert response.status_code == 200
    
    for genpost in [genpost_1, genpost_2, genpost_3]:
        assert genpost.model_dump() in response.json['favorites']

def test_get_favorite_public_official_empty(client, auth):
    # Test adding public official to favorites
    auth.create_basic_user()
    
    response = client.get(f'user/favorites/public_official', headers=auth.get_auth_header())
    
    assert response.status_code == 200
    
    assert response.json['favorites'] == []
    

def test_get_favorite_generated_post_empty(client, auth, public_official_actions):
    # Test adding generated post to favorites
    public_official_id = public_official_actions.create_public_official().get_id()
    
    auth.create_basic_user()
    
    response = client.get(f'user/favorites/generated_post', headers=auth.get_auth_header())
    
    assert response.status_code == 200
    
    assert response.json['favorites'] == []

def test_get_invalid_favorite_type(client, auth):
    # Test getting invalid favorite type
    auth.create_basic_user()

    response = client.get(f'user/favorites/invalid', headers=auth.get_auth_header())

    assert response.status_code == 404 # Not Found
