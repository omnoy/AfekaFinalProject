from app.logic.mongo.database import get_generated_post_collection

def test_delete_all_generated_posts(client, auth, public_official_actions):
    # Test to delete all generated posts
    po_id = public_official_actions.create_public_official().get_id()
    
    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "facebook"}

    auth.create_basic_user()

    client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())
    # TODO replace with fake api calls

    auth.create_admin_user()

    response = client.delete(f"/postgeneration/posts/history/all", headers=auth.get_auth_header())

    assert response.status_code == 200

    assert len(list(get_generated_post_collection().find({}))) == 0
    
def test_delete_all_generated_posts_empty(client, auth):
    # Test to delete all generated posts when there are none
    auth.create_admin_user()

    response = client.delete(f"/postgeneration/posts/history/all", headers=auth.get_auth_header())

    assert response.status_code == 200
    assert len(list(get_generated_post_collection().find({}))) == 0

def test_get_user_generated_post_history_unauthorized(client, auth, public_official_actions):
    # Test to delete all generated posts by user id without authorization (not an admin)
    po_id = public_official_actions.create_public_official().get_id()
    
    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "po_id": po_id, 
                   "social_media": "facebook"}

    auth.create_basic_user()

    client.post("/postgeneration/generate", json=prompt_dict, headers=auth.get_auth_header())

    response = client.delete(f"/postgeneration/posts/history/all", headers=auth.get_auth_header())

    assert response.status_code == 403

    assert len(list(get_generated_post_collection().find({}))) == 1

