def test_creation(client):
    response = client.get("/users")
    #assert 