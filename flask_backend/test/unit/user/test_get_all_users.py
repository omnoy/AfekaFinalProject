import json

def test_get_all_users(client, auth):
    # Test getting all users
    auth.create(email="one@mail.com")
    auth.create(email="two@mail.com")
    auth.create(email="three@mail.com")

    auth.create_admin()

    response = client.get("/user/all", headers={'Authorization': auth.access_token})

    assert response.status_code == 200
    assert len(json.loads(response.json['users'])) == 4

def test_get_all_users_unauthorized(client, auth):
    # Test getting all users
    auth.create(email="one@mail.com")
    auth.create(email="two@mail.com")
    auth.create(email="three@mail.com")

    auth.create()

    response = client.get("/user/all", headers={'Authorization': auth.access_token})

    assert response.status_code == 403