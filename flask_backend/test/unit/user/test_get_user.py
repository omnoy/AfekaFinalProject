def test_get_user(client, auth):
    # Test getting a user
    user_dict = auth.create_basic_user()['response'].json['user']
    
    response = client.get("/user/get", headers=auth.get_auth_header())
    
    assert response.status_code == 200
    
    response_user_dict = response.json['user']
    
    assert user_dict == response_user_dict

def test_get_user_unauthorized(client, auth):
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxODA3MjgxMiwianRpIjoiOWJlZTU1NTctYWNlYS00NzhkLWEyMTQtMmE5OGVjMGVkNGE2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY2NjdiNWVjZGM0YjY3N2EzM2FkNjQ5NSIsIm5iZiI6MTcxODA3MjgxMiwiY3NyZiI6Ijc2YmVlZGY3LWMxYTAtNGIxOS1iNjkzLWM5NWU3MTNlNWRmNSIsImV4cCI6MTcxODA3MzcxMn0.tpGKxrLC8bXAFS5MKw7as2Bu_-OURcD0XaRkR-kNBPU"
    response = client.get("/user/get", headers=auth.get_auth_header(invalid_token))
    
    assert response.status_code == 401