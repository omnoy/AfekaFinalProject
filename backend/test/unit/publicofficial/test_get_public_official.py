def test_get_public_official_by_id(client, auth, public_official_actions):
    # Find valid Public Official by ID
    auth.create_admin_user()

    public_official = public_official_actions.create_public_official()

    response = client.get(f"/public-official/get/{public_official.get_id()}", headers=auth.get_auth_header())

    assert response.status_code == 200
    
    response_dict = response.json['public_official']

    assert response_dict == public_official.model_dump()

def test_get_public_official_with_invalid_id(client, auth):
    # Find valid Public Official by ID
    response = auth.create_admin_user()
    invalid_id = '666d7c070477c0def6d136c9'

    response = client.get(f"/public-official/get/{invalid_id}", headers=auth.get_auth_header())

    assert response.status_code == 404