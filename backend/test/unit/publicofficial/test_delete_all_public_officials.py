from app.logic.mongo.database import get_public_official_collection

def test_delete_all_public_officials(client, auth, public_official_actions):
    auth.create_admin_user()

    public_official_actions.create_public_official()
    public_official_actions.create_public_official(full_name={"eng": "testman the second", "heb": "טסטמן השני"})
    public_official_actions.create_public_official(full_name={"eng": "testman the third", "heb": "טסטמן השלישי"})
    
    response = client.delete("/public-official/all", headers=auth.get_auth_header())

    assert response.status_code == 200

    assert len(list(get_public_official_collection().find({}))) == 0

def test_delete_all_public_officials_unauthorized(client, auth, public_official_actions):
    auth.create_admin_user()

    public_official_actions.create_public_official()
    public_official_actions.create_public_official(full_name={"eng": "testman the second", "heb": "טסטמן השני"})
    public_official_actions.create_public_official(full_name={"eng": "testman the third", "heb": "טסטמן השלישי"})
    
    auth.create_basic_user()

    response = client.delete("/public-official/all", headers=auth.get_auth_header())

    assert response.status_code == 401

    assert len(list(get_public_official_collection().find({}))) == 3