from app.models.user import User
import json

def test_create_user(client, app):
    response = client.post("/users", content_type='application/json', data=json.dumps({"username": "testman", "password": "test", "personal_name": "test", "email": "test@test.com", "role": "basic_user"}))
    print(response.data)
    assert response.data[0]['username'] == 'testman'
    

    
def test_login_user(client, app):
    # 
    # 

    # assert len(json.loads(response.data)) == 1
    pass