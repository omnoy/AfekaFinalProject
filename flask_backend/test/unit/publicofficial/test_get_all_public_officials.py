import json


def test_get_all_public_officials(client, auth):
    # Test case: Get all public officials
    auth.create_admin_user()

    po_dict_1 = {
        "name_eng": "testman", 
        "name_heb": "טסטמן", 
        "position": "ראש הטסטים", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman"}
    }

    po_dict_2 = {
        "name_eng": "testman the second", 
        "name_heb": "טסטמן השני", 
        "position": "ראש הטסטים שתיים", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman"}
    }

    po_dict_3 = {
        "name_eng": "testman the third", 
        "name_heb": "טסטמן השלישי", 
        "position": "ראש הטסטים שלוש", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman"}
    }

    client.post("/public-official/create", json=po_dict_1, headers=auth.get_auth_header())
    client.post("/public-official/create", json=po_dict_2, headers=auth.get_auth_header())
    client.post("/public-official/create", json=po_dict_3, headers=auth.get_auth_header())

    response = client.get("/public-official/all", headers=auth.get_auth_header())

    assert response.status_code == 200

    response_po_list = response.json['public_officials']
    
    assert len(response_po_list) ==  3

    for po in response_po_list:
        po = dict(po)
        po.pop('id')
        assert po in [po_dict_1, po_dict_2, po_dict_3]

def test_get_all_public_officials_empty(client, auth):
    auth.create_admin_user()
    
    response = client.get("/public-official/all", headers=auth.get_auth_header())

    assert response.status_code == 200

    response_po_list = response.json['public_officials']

    assert len(response_po_list) ==  0

def test_get_all_public_officials_unauthorized(client, auth):
    auth.create_basic_user()

    response = client.get("/public-official/all", headers=auth.get_auth_header())

    assert response.status_code == 401