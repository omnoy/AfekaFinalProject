def test_add_favorite_public_official(client, auth, public_official_actions):
    # Test adding public official to favorites
    po_id = public_official_actions.create_public_official().get_id()
    
    auth.create_basic_user()

    response = client.put(f'user/favorites/public_official?object_id={po_id}', headers=auth.get_auth_header())

    assert response.status_code == 200

    user = auth.login()['response'].json['user']
    assert po_id in user['favorites']['public_official']

def test_add_favorite_generated_post(client, auth, public_official_actions):
    # Test adding generated post to favorites
    po_id = public_official_actions.create_public_official().get_id()
    
    auth.create_basic_user()

    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "facebook"}
    
    response = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    
    genpost_id = response.json["generated_post"]["id"]

    response = client.put(f'user/favorites/generated_post?object_id={genpost_id}', headers=auth.get_auth_header())

    assert response.status_code == 200

    user = auth.login()['response'].json['user']
    assert genpost_id in user['favorites']['generated_post']

def test_add_favorite_generated_post_unauthorized(client, auth, public_official_actions):
    # Test adding generated post of another user to favorites (unauthorized)
    po_id = public_official_actions.create_public_official().get_id()
    
    auth.create_basic_user()

    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "facebook"}
    
    response = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    
    genpost_id = response.json["generated_post"]["id"]

    auth.create_basic_user(email="test2@gmail.com")

    response = client.put(f'user/favorites/generated_post?object_id={genpost_id}', headers=auth.get_auth_header())

    assert response.status_code == 403

def test_add_favorite_public_official_invalid_id(client, auth):
    # Test adding public official to favorites with an invalid id
    auth.create_basic_user()

    response = client.put(f'user/favorites/public_official?object_id=667197af047f22ff2e4054bd', headers=auth.get_auth_header())

    assert response.status_code == 400

def test_add_favorite_generated_post_invalid_id(client, auth):
    # Test adding public official to favorites with an invalid id
    auth.create_basic_user()

    response = client.put(f'user/favorites/generated_post?object_id=667197af047f22ff2e4054bd', headers=auth.get_auth_header())

    assert response.status_code == 400