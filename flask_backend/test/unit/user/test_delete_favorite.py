def test_removing_favorite_public_official(client, auth, public_official_actions):
    # Test removing a public official from favorites
    po_id = public_official_actions.create_public_official().get_id()
    
    auth.create_basic_user()

    client.put(f'user/favorites/public_official?object_id={po_id}', headers=auth.get_auth_header())

    response = client.delete(f'user/favorites/public_official?object_id={po_id}', headers=auth.get_auth_header())

    assert response.status_code == 200

    user = auth.login()['response'].json['user']
    assert po_id not in user['favorites']['public_official']

def test_remove_favorite_generated_post(client, auth, public_official_actions):
    # Test removing generated post from favorites
    po_id = public_official_actions.create_public_official().get_id()
    
    auth.create_basic_user()

    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "facebook"}
    
    response = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    
    genpost_id = response.json["generated_post"]["id"]

    response = client.put(f'user/favorites/generated_post?object_id={genpost_id}', headers=auth.get_auth_header())

    response = client.delete(f'user/favorites/generated_post?object_id={genpost_id}', headers=auth.get_auth_header())

    assert response.status_code == 200

    user = auth.login()['response'].json['user']
    assert genpost_id not in user['favorites']['generated_post']

def test_remove_favorite_public_official_invalid_id(client, auth):
    # Test removing public official to favorites with an invalid id
    auth.create_basic_user()

    response = client.delete(f'user/favorites/public_official?object_id=667197af047f22ff2e4054bd', headers=auth.get_auth_header())

    assert response.status_code == 400

def test_remove_favorite_generated_post_invalid_id(client, auth):
    # Test removing public official to favorites with an invalid
    auth.create_basic_user()

    response = client.delete(f'user/favorites/generated_post?object_id=667197af047f22ff2e4054bd', headers=auth.get_auth_header())

    assert response.status_code == 400