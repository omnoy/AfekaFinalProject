def test_get_generated_post_by_post_id(client, auth, public_official_actions):
    # Test to get a generated post by post id
    po_id = public_official_actions.create_public_official().get_id()

    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "facebook"}

    auth.create_basic_user()

    generated_post = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    # TODO replace with fake api calls

    genpost_id = generated_post.json["generated_post"]["id"]

    response = client.get(f"/postgeneration/posts/{genpost_id}", headers=auth.get_auth_header())

    assert response.status_code == 200
    assert response.json["generated_post"] == generated_post.json["generated_post"]

def test_get_generated_post_by_post_id_admin(client, auth, public_official_actions):
    # Test to get a generated post by post id from a different user as an admin 
    po_id = public_official_actions.create_public_official().get_id()

    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "facebook"}

    auth.create_basic_user()

    generated_post = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    # TODO replace with fake api calls

    genpost_id = generated_post.json["generated_post"]["id"]

    auth.create_admin_user()

    response = client.get(f"/postgeneration/posts/{genpost_id}", headers=auth.get_auth_header())

    assert response.status_code == 200
    assert response.json["generated_post"] == generated_post.json["generated_post"]

def test_get_generated_post_by_post_id_not_found(client, auth):
    # Test to get a generated post by post id that does not exist
    auth.create_basic_user()

    response = client.get("/postgeneration/posts/6670be79761f0759941c494c", headers=auth.get_auth_header())

    assert response.status_code == 404

def test_get_generated_post_by_post_id_unauthorized(client, auth, public_official_actions):
    # Test to get a generated post by post id without authorization (not an admin)
    po_id = public_official_actions.create_public_official().get_id()

    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "facebook"}

    auth.create_basic_user()

    response = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    # TODO replace with fake api calls

    genpost_id = response.json["generated_post"]["id"]

    auth.create_basic_user(email='test2@test.com') #other unauthorized user

    response = client.get(f"/postgeneration/posts/{genpost_id}", headers=auth.get_auth_header())

    assert response.status_code == 403