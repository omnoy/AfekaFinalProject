def test_generate_post(client, auth, public_official_actions):
    # Test Post Generation
    po_id = public_official_actions.create_public_official().get_id()

    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "facebook"}

    auth.create_basic_user()

    response = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    #TODO when using api use fake api calls

    assert response.status_code == 200

    assert response.json["generated_post"]["title"] == "Jeff: the Post"

    assert response.json["generated_post"]["text"] == "my name jeff"
    assert response.json["generated_post"]["user_id"] == auth.get_user_id()
    assert response.json["generated_post"]["public_official_id"] == po_id
    
def test_generate_post_with_invalid_po_id(client, auth):
    # Test Post Generation with an invalid po_id
    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": "666e3cdc77f6b009eab6d345", #invalid
                   "social_media": "FACEBOOK"} 
             
    auth.create_basic_user()

    response = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())

    assert response.status_code == 404

def test_generate_post_with_empty_prompt(client, auth, public_official_actions):
    po_id = public_official_actions.create_public_official().get_id()

    prompt_dict = {"generation_prompt": "", 
                   "po_id": po_id, 
                   "social_media": "facebook"}

    auth.create_basic_user()

    response = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    #TODO when using api use fake api calls

    assert response.status_code == 400

def test_generate_post_with_invalid_social_media(client, auth, public_official_actions):
    po_id = public_official_actions.create_public_official().get_id()

    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "test"} #invalid

    auth.create_basic_user()

    response = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())

    assert response.status_code == 400