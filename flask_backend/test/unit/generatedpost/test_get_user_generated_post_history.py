def test_get_user_generated_post_history(client, auth, public_official_actions):
    # Test to get all generated posts by user id
    po_id = public_official_actions.create_public_official().get_id()

    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "facebook"}

    auth.create_basic_user()

    generated_post = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())

    prompt_dict["generation_prompt"] = "Make a post about Jeff again."

    generated_post2 = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())

    prompt_dict["generation_prompt"] = "Make a post about Jeff a third time."

    generated_post3 = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    # TODO replace with fake api calls

    response = client.get(f"/postgeneration/posts/history/{auth.get_user_id()}", headers=auth.get_auth_header())

    assert response.status_code == 200
    for generated_post in response.json["generated_posts"]:
        assert generated_post in [generated_post.json["generated_post"] for generated_post in [generated_post, generated_post2, generated_post3]]

def test_get_user_generated_post_history_admin(client, auth, public_official_actions):
    # Test to get all generated posts by user id as an admin
    po_id = public_official_actions.create_public_official().get_id()

    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "facebook"}

    auth.create_basic_user()

    generated_post = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())

    prompt_dict["generation_prompt"] = "Make a post about Jeff again."

    generated_post2 = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())

    prompt_dict["generation_prompt"] = "Make a post about Jeff a third time."

    generated_post3 = client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    # TODO replace with fake api calls
    user_id = auth.get_user_id()

    auth.create_admin_user()

    response = client.get(f"/postgeneration/posts/history/{user_id}", headers=auth.get_auth_header())

    assert response.status_code == 200
    for generated_post in response.json["generated_posts"]:
        assert generated_post in [generated_post.json["generated_post"] for generated_post in [generated_post, generated_post2, generated_post3]]

def test_get_user_generated_post_history_empty(client, auth):
    # Test to get all generated posts by user id that does not exist
    auth.create_basic_user()

    response = client.get(f"/postgeneration/posts/history/{auth.get_user_id()}", headers=auth.get_auth_header())

    assert response.status_code == 200
    assert response.json["generated_posts"] == []

def test_get_user_generated_post_history_unauthorized(client, auth):
    # Test to get all generated posts by user id without authorization (not an admin)
    auth.create_basic_user()

    response = client.get(f"/postgeneration/posts/history/6670be79761f0759941c494c", headers=auth.get_auth_header())

    assert response.status_code == 403

