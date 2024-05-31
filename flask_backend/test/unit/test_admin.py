import json

def test_get_all_users(client):
    response = client.get("/users")
    assert len(json.loads(response.data)) == 0

def test_delete_all_users(client):
    
    response = client.delete("/users")
