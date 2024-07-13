def test_get_generated_post_by_post_id(client, auth, public_official_actions, generated_post_actions):
    # Test to get a generated post by post id
    
    auth.create_basic_user()
    
    user_id = auth.get_user_id()
    
    public_official_id = public_official_actions.create_public_official().get_id()    

    generated_post = generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)

    response = client.get(f"/post-generation/posts/{generated_post.get_id()}", headers=auth.get_auth_header())

    assert response.status_code == 200
    assert response.json["generated_post"] == generated_post.model_dump()

def test_get_generated_post_by_post_id_admin(client, auth, public_official_actions, generated_post_actions):
    # Test to get a generated post by post id from a different user as an admin 
    
    auth.create_basic_user()
    
    user_id = auth.get_user_id()
    
    public_official_id = public_official_actions.create_public_official().get_id()

    generated_post = generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)

    auth.create_admin_user()

    response = client.get(f"/post-generation/posts/{generated_post.get_id()}", headers=auth.get_auth_header())

    assert response.status_code == 200
    assert response.json["generated_post"] == generated_post.model_dump()

def test_get_generated_post_by_post_id_not_found(client, auth):
    # Test to get a generated post by post id that does not exist
    auth.create_basic_user()

    response = client.get("/post-generation/posts/6670be79761f0759941c494c", headers=auth.get_auth_header())

    assert response.status_code == 404

def test_get_generated_post_by_post_id_unauthorized(client, auth, public_official_actions, generated_post_actions):
    # Test to get a generated post by post id without authorization (not an admin)
    
    auth.create_basic_user()
    
    user_id = auth.get_user_id()
    
    public_official_id = public_official_actions.create_public_official().get_id()

    generated_post = generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)

    auth.create_basic_user(email='test2@test.com') #other unauthorized user

    response = client.get(f"/post-generation/posts/{generated_post.get_id()}", headers=auth.get_auth_header())

    assert response.status_code == 403