import json


def test_get_public_official_by_id(client, auth):
    # Find valid Public Official by ID
    auth.create_admin_user()

    po_dict = {
        "name_eng": "testman", 
        "name_heb": "טסטמן", 
        "position": "ראש הטסטים", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }

    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())
    
    public_official_id = response.json['public_official']['id']

    response = client.get(f"/public-official/get/{public_official_id}", headers=auth.get_auth_header())

    assert response.status_code == 200
    
    response_dict = response.json['public_official']
    response_dict.pop('id')

    assert response_dict == po_dict

def test_get_public_official_with_invalid_id(client, auth):
    # Find valid Public Official by ID
    response = auth.create_admin_user()
    invalid_id = '666d7c070477c0def6d136c9'

    response = client.get(f"/public-official/get/{invalid_id}", headers=auth.get_auth_header())

    assert response.status_code == 404