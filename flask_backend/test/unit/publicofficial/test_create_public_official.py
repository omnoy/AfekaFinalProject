import json
from app.logic.mongo.database import get_public_official_collection

def test_create_public_official(client, auth):
    # Test case: Create a public official with valid data
    auth.create_admin_user()

    po_dict = {
        "name_eng": "testman", 
        "name_heb": "טסטמן", 
        "position": "ראש הטסטים", 
        "political_party": "טסט פארטי", 
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }

    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 200

    response_po_dict = response.json['public_official']
    response_po_dict.pop('id')
    assert response_po_dict == po_dict

    db_po_dict = get_public_official_collection().find_one({"name_eng":"testman"})
    db_po_dict.pop('_id')

    assert db_po_dict == po_dict

def test_create_public_official_missing_fields(client, auth):
    # Test case: Create a public official with missing required fields

    auth.create_admin_user()

    po_dict = {
        "name_eng": "testman",
        "position": "ראש הטסטים",
        "political_party": "טסט פארטי",
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }
    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())
    assert response.status_code == 400

def test_create_public_official_invalid_name_eng(client, auth):
    # Test case: Create a public official with invalid name_eng

    auth.create_admin_user()

    po_dict = {
        "name_eng": "test123",
        "name_heb": "טסטמן",
        "position": "ראש הטסטים",
        "political_party": "טסט פארטי",
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }
    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())
    assert response.status_code == 400

def test_create_public_official_invalid_name_heb(client, auth):
    # Test case: Create a public official with invalid name_heb

    auth.create_admin_user()

    po_dict = {
        "name_eng": "testman",
        "name_heb": "טסט234manמן",
        "position": "ראש הטסטים",
        "political_party": "טסט פארטי",
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }
    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())
    assert response.status_code == 400

def test_create_public_official_invalid_position(client, auth):
    # Test case: Create a public official with invalid position

    auth.create_admin_user()

    po_dict = {
        "name_eng": "testman",
        "name_heb": "טסטמן",
        "position": "badposition",
        "political_party": "טסט פארטי",
        "social_media_handles": {"twitter": "testman", "facebook": "testman"}
    }
    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())
    assert response.status_code == 400

def test_create_public_official_invalid_social_media_handles(client, auth):
    # Test case: Create a public official with invalid social_media_handles

    auth.create_admin_user()

    po_dict = {
        "name_eng": "testman",
        "name_heb": "טסטמן",
        "position": "ראש הטסטים",
        "political_party": "טסט פארטי",
        "social_media_handles": {"twitter": "test", "myspace": "testman"}
    }
    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())
    assert response.status_code == 400

def test_create_existing_public_official(client, auth):
    # Test case: Create a public official with invalid social_media_handles

    auth.create_admin_user()

    po_dict = {
        "name_eng": "testman",
        "name_heb": "טסטמן",
        "position": "ראש הטסטים",
        "political_party": "טסט פארטי",
        "social_media_handles": {"twitter": "test", "facebook": "testman"}
    }
    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())
    assert response.status_code == 200

    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())
    assert response.status_code == 409