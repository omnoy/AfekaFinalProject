def test_login_user(client, auth):
    login_info = {"email":"test@test.com", "password": "testtest"}

    auth.create_basic_user(**login_info)
    
    response = client.post("/auth/login", json=login_info)

    assert response.status_code == 200

def test_login_user_invalid_email(client, auth):
    auth.create_basic_user()

    login_info = {"email": "invalidemailaddress", "password": "testtest"}

    response = client.post("/auth/login", json=login_info)

    assert response.status_code == 401

def test_login_user_invalid_password(client, auth):
    auth.create_basic_user()

    login_info = {"email": "test@test.com", "password": "wrongpassword"}

    response = client.post("/auth/login", json=login_info)

    assert response.status_code == 401