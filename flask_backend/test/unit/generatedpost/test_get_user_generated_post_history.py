def test_get_user_generated_post_history(client, auth, public_official_actions, generated_post_actions):
    # Test to get all generated posts by user id
    auth.create_basic_user()
    user_id = auth.get_user_id()
    
    public_official_id = public_official_actions.create_public_official().get_id()

    generated_post_1 = generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)
    generated_post_2 = generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)
    generated_post_3 = generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)

    response = client.get(f"/post-generation/posts/user", headers=auth.get_auth_header())
    
    assert response.status_code == 200
    for generated_post in [generated_post_1, generated_post_2, generated_post_3]:
        assert generated_post.model_dump() in response.json["generated_posts"]

def test_get_user_generated_post_history_empty(client, auth):
    # Test to get all generated posts by user id that does not exist
    auth.create_basic_user()

    response = client.get(f"/post-generation/posts/user", headers=auth.get_auth_header())

    assert response.status_code == 200
    assert response.json["generated_posts"] == []
