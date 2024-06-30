from app.logic.mongo.database import get_generated_post_collection

def test_delete_all_generated_posts(client, auth, public_official_actions, generated_post_actions):
    # Test to delete all generated posts
    auth.create_basic_user()
    
    user_id = auth.get_user_id()
    
    public_official_id = public_official_actions.create_public_official().get_id()
    
    generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)
    generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)
    generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)

    auth.create_admin_user()

    response = client.delete(f"/post-generation/posts/all", headers=auth.get_auth_header())

    assert response.status_code == 200

    assert len(list(get_generated_post_collection().find({}))) == 0
    
def test_delete_all_generated_posts_empty(client, auth):
    # Test to delete all generated posts when there are none
    auth.create_admin_user()

    response = client.delete(f"/post-generation/posts/all", headers=auth.get_auth_header())

    assert response.status_code == 200
    assert len(list(get_generated_post_collection().find({}))) == 0

def test_get_user_generated_post_history_unauthorized(client, auth, public_official_actions, generated_post_actions):
    # Test to delete all generated posts by user id without authorization (not an admin)
    
    auth.create_basic_user()
    
    user_id = auth.get_user_id()
    
    public_official_id = public_official_actions.create_public_official().get_id()
    
    generated_post_actions.create_generated_post(user_id=user_id, public_official_id=public_official_id)

    response = client.delete(f"/post-generation/posts/all", headers=auth.get_auth_header())

    assert response.status_code == 401

    assert len(list(get_generated_post_collection().find({}))) == 1

