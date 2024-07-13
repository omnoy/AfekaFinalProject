from app.logic.mongo.database import get_token_blocklist

def test_logout_user(client, auth):
    # Test case 1: Logout with a valid token
    user_result = auth.create_basic_user()
    
    response = client.post("/auth/logout", headers=auth.get_auth_header())

    assert response.status_code == 200
    
    token_blocked_list = list(get_token_blocklist().find({}))
    
    assert len(token_blocked_list) == 1

def test_logout_user_invalid_token(client, auth):
    # Test case 2: Logout with an invalid token
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxODA3MjgxMiwianRpIjoiOWJlZTU1NTctYWNlYS00NzhkLWEyMTQtMmE5OGVjMGVkNGE2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY2NjdiNWVjZGM0YjY3N2EzM2FkNjQ5NSIsIm5iZiI6MTcxODA3MjgxMiwiY3NyZiI6Ijc2YmVlZGY3LWMxYTAtNGIxOS1iNjkzLWM5NWU3MTNlNWRmNSIsImV4cCI6MTcxODA3MzcxMn0.tpGKxrLC8bXAFS5MKw7as2Bu_-OURcD0XaRkR-kNBPU"
    response = client.post("/auth/logout", headers=auth.get_auth_header(invalid_token))
    assert response.status_code == 401 # Unauthorized

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