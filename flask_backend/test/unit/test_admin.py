import json

def test_get_all_users(client):
    response = client.get("/user")

def test_delete_all_users(client):
    response = client.delete("/user")
