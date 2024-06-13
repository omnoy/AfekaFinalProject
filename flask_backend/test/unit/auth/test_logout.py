def test_logout_user(client, auth):
    # Test case 1: Logout with a valid token
    user_result = auth.create()
    headers = {'Authorization': 'Bearer ' + user_result.json['access_token']}
    response = client.post("/auth/logout", headers=headers)

    assert response.status_code == 200

def test_logout_user_invalid_token(client):
    # Test case 2: Logout with an invalid token
    invalid_token = "invalid_token"
    headers = {'Authorization': 'Bearer ' + invalid_token}
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 422 # Unprocessable Entity

def test_logout_user_no_token(client):
    # Test case 3: Logout without providing a token
    response = client.post("/auth/logout")
    assert response.status_code == 401  # Unauthorized

def test_logout_user_double_logout(client, auth):
    # Test case 4: Logout after logging out (double logout)
    user_result = auth.create()
    headers = {'Authorization': 'Bearer ' + user_result.json['access_token']}
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 401  # Unauthorized

def test_logout_user_expired_token(client, auth):
    # Test case 5: Logout with an expired token
    user_result = auth.create()
    headers = {'Authorization': 'Bearer ' + user_result.json['access_token']}
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200

    user_result = auth.login()
    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 401  # Unauthorized