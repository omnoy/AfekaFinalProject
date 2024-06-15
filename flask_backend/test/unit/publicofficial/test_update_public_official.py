import json
from app.logic.mongo.database import get_public_official_collection

def test_update_public_official(client, auth):
    # Test case: Update a public official with valid data
    auth.create_admin()

    po_dict = {
        "name_eng": "testman", 
        "name_heb": "טסטמן", 
        "position": "ראש הטסטים", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }

    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())

    po_id = response.json['public_official']['id']

    po_dict['name_eng'] = 'newname'
    po_dict['name_heb'] = 'שםחדש'

    response = client.put(f"/public-official/update/{po_id}", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 200

    response_po_dict = response.json['public_official']
    response_po_dict.pop('id')
    assert response_po_dict == po_dict

    db_po_dict = get_public_official_collection().find_one({"name_eng":"newname"})
    db_po_dict.pop('_id')

    assert db_po_dict == po_dict

def test_update_public_official_missing_fields(client, auth):
    # Test case: Update a public official with missing fields
    auth.create_admin()

    po_dict = {
        "name_eng": "testman", 
        "name_heb": "טסטמן", 
        "position": "ראש הטסטים", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }

    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())

    po_id = response.json['public_official']['id']

    po_dict.pop('position')

    response = client.put(f"/public-official/update/{po_id}", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 400

def test_update_public_official_invalidid(client, auth):
    # Test case: Update a public official with missing fields
    auth.create_admin()

    po_dict = {
        "name_eng": "testman", 
        "name_heb": "טסטמן", 
        "position": "ראש הטסטים", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }

    response = client.put(f"/public-official/update/666d7c070477c0def6d136c9", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 404

def test_update_public_official_invalid_name_eng(client, auth):
    # Test case: Update a public official with invalid English name
    auth.create_admin()

    po_dict = {
        "name_eng": "testman", 
        "name_heb": "טסטמן", 
        "position": "ראש הטסטים", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }

    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())

    po_id = response.json['public_official']['id']

    po_dict['name_eng'] = 'newname123'

    response = client.put(f"/public-official/update/{po_id}", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 400

def test_update_public_official_invalid_name_heb(client, auth):
    # Test case: Update a public official with invalid Hebrew name
    auth.create_admin()

    po_dict = {
        "name_eng": "testman", 
        "name_heb": "טסטמן", 
        "position": "ראש הטסטים", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }

    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())

    po_id = response.json['public_official']['id']

    po_dict['name_heb'] = 'טסטי134man'

    response = client.put(f"/public-official/update/{po_id}", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 400

def test_update_public_official_invalid_position(client, auth):
    # Test case: Update a public official with invalid position
    auth.create_admin()

    po_dict = {
        "name_eng": "testman", 
        "name_heb": "טסטמן", 
        "position": "ראש הטסטים", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }

    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())

    po_id = response.json['public_official']['id']

    po_dict['position'] = 'myposition123'

    response = client.put(f"/public-official/update/{po_id}", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 400

def test_update_public_official_invalid_social_media_handles(client, auth):
    # Test case: Update a public official with invalid social media handles
    auth.create_admin()

    po_dict = {
        "name_eng": "testman", 
        "name_heb": "טסטמן", 
        "position": "ראש הטסטים", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }

    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())

    po_id = response.json['public_official']['id']

    po_dict['social_media_handles']['myspace'] = 'myhandle'

    response = client.put(f"/public-official/update/{po_id}", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 400