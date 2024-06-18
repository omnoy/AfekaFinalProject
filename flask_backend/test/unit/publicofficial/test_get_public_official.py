import json


def test_get_public_official_byid(client, auth):
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
    
    po_id = response.json['public_official']['id']

    response = client.get(f"/public-official/get/{po_id}")

    assert response.status_code == 200
    
    response_dict = response.json['public_official']
    response_dict.pop('id')

    assert response_dict == po_dict

def test_get_public_official_with_invalidid(client, auth):
    # Find valid Public Official by ID
    response = auth.create_admin_user()
    invalidid = '666d7c070477c0def6d136c9'

    response = client.get(f"/public-official/get/{invalidid}")

    assert response.status_code == 404