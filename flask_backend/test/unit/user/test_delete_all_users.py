from app.logic.mongo.database import get_user_collection
def test_delete_all_users(client, auth):
    # Test deleting all users
    auth.create(email="one@mail.com")
    auth.create(email="two@mail.com")
    auth.create(email="three@mail.com")

    auth.create_admin()

    response = client.delete("/user/all", headers={'Authorization': auth.access_token})

    assert response.status_code == 200

    assert len(list(get_user_collection().find())) == 0

def test_delete_all_users_unauthorized(client, auth):
    # Test deleting all users
    auth.create(email="one@mail.com")
    auth.create(email="two@mail.com")
    auth.create(email="three@mail.com")

    auth.create()

    response = client.delete("/user/all", headers={'Authorization': auth.access_token})

    assert response.status_code == 403