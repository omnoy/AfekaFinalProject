import json

def test_get_all_users(client, auth):
    # Test getting all users
    userlist = []
    response = auth.create_basic_user(email="one@mail.com")["response"]
    userlist.append(response.json['user'])

    response = auth.create_basic_user(email="two@mail.com")["response"]
    userlist.append(response.json['user'])

    response = auth.create_basic_user(email="three@mail.com")["response"]
    userlist.append(response.json['user'])

    response = auth.create_admin_user()["response"]
    userlist.append(response.json['user'])

    response = client.get("/user/all", headers=auth.get_auth_header())

    assert response.status_code == 200
    response_userlist = response.json['users']
    assert len(userlist) == 4
    for response_user in response_userlist:
        response_user = dict(response_user)
        assert response_user in userlist

def test_get_all_users_unauthorized(client, auth):
    # Test getting all users as a basic user
    auth.create_basic_user(email="one@mail.com")
    auth.create_basic_user(email="two@mail.com")
    auth.create_basic_user(email="three@mail.com")

    auth.create_basic_user()

    response = client.get("/user/all", headers=auth.get_auth_header())

    assert response.status_code == 401 # Forbidden