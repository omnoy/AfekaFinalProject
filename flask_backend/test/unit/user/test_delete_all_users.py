from app.logic.mongo.database import get_user_collection
def test_delete_all_users(client, auth):
    # Test deleting all users
    auth.create_basic_user(email="one@mail.com")
    auth.create_basic_user(email="two@mail.com")
    auth.create_basic_user(email="three@mail.com")

    auth.create_admin_user()

    response = client.delete("/user/all", headers=auth.get_auth_header())

    assert response.status_code == 200

    assert len(list(get_user_collection().find())) == 0

def test_delete_all_users_unauthorized(client, auth):
    # Test deleting all users
    auth.create_basic_user(email="one@mail.com")
    auth.create_basic_user(email="two@mail.com")
    auth.create_basic_user(email="three@mail.com")

    auth.create_basic_user()

    response = client.delete("/user/all", headers=auth.get_auth_header())

    assert response.status_code == 401 # Unauthorized