def test_logout_user(client, auth):
    # Test case 1: Logout with a valid token
    user_result = auth.create_basic_user()
    response = client.post("/auth/logout", headers=auth.get_auth_header())

    assert response.status_code == 200

def test_logout_user_invalid_token(client, auth):
    # Test case 2: Logout with an invalid token
    invalid_token = "invalid_token"
    response = client.post("/auth/logout", headers=auth.get_auth_header(invalid_token))
    assert response.status_code == 422 # Unprocessable Entity

def test_logout_user_no_token(client):
    # Test case 3: Logout without providing a token
    response = client.post("/auth/logout")
    assert response.status_code == 401  # Unauthorized

def test_logout_user_double_logout(client, auth):
    # Test case 4: Logout after logging out (double logout)
    auth.create_basic_user()
    response = client.post("/auth/logout", headers=auth.get_auth_header())
    assert response.status_code == 200
    response = client.post("/auth/logout", headers=auth.get_auth_header())
    assert response.status_code == 401  # Unauthorized

def test_logout_user_expired_token(client, auth):
    # Test case 5: Logout with an expired token
    response = auth.create_basic_user()
    expired_token = response['access_token']
    response = client.post("/auth/logout", headers=auth.get_auth_header())
    assert response.status_code == 200

    auth.login()
    response = client.post("/auth/logout", headers=auth.get_auth_header(expired_token))
    assert response.status_code == 401  # Unauthorized