import json
from app.logic.mongo.database import get_public_official_collection

po_dict_template = {
    "full_name": 
    {
        "eng": "testman",
        "heb": "טסטמן"
    },
    "age": 30,
    "position": 
    {
        "eng": "Lead Tester",
        "heb": "ראש הטסטים"
    },
    "political_party": 
    {
        "eng": "Test Party",
        "heb": "טסט פארטי"
    }, 
    "social_media_handles": 
    {
        "twitter": "testman", 
        "facebook": "testman"
    }
}

def test_create_public_official(client, auth):
    # Test case: Create a public official with valid data
    auth.create_admin_user()

    po_dict = po_dict_template.copy()

    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 200

    response_po_dict = response.json['public_official']
    response_po_dict.pop('id')
    
    assert response_po_dict == po_dict

    db_po_dict = get_public_official_collection().find_one({"full_name":{"eng": "testman", "heb": "טסטמן"}})
    db_po_dict.pop('_id')

    assert db_po_dict == po_dict

def test_create_public_official_unauthorized(client, auth):
    # Test case: Create a public official with valid data
    auth.create_basic_user()
    
    po_dict = po_dict_template.copy()

    response = client.post("/public-official/create", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 401

def test_create_public_official_missing_fields(client, auth):
    # Test case: Create a public official with missing required fields

    auth.create_admin_user()

    po_dict = po_dict_template.copy()
    
    for key in ['full_name', 'position']:
        temp_dict = po_dict.copy()
        temp_dict.pop(key)
        response = client.post("/public-official/create", json=temp_dict, headers=auth.get_auth_header())
        assert response.status_code == 400

def test_create_public_official_invalid_full_name(client, auth):
    # Test case: Create a public official with invalid full name
    auth.create_admin_user()

    for eng_name in ['123', '', 'שם בעברית', 'שם בעברית123']:
        po_dict_copy = po_dict_template.copy()
        po_dict_copy['full_name']['eng'] = eng_name
        response = client.post(f"/public-official/create", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

    for heb_name in ['123', '', 'english name', 'english name123']:
        po_dict_copy = po_dict_template.copy()
        po_dict_copy['full_name']['heb'] = heb_name
        response = client.post("/public-official/create", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

def test_update_public_official_invalid_position(client, auth):
    # Test case: Create a public official with invalid position
    auth.create_admin_user()

    for eng_position in ['', 'תפקיד בעברית']:
        po_dict_copy = po_dict_template.copy()
        po_dict_copy['position']['eng'] = eng_position
        response = client.post("/public-official/create", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

    for heb_position in ['', 'english position']:
        po_dict_copy = po_dict_template.copy()
        po_dict_copy['position']['heb'] = heb_position
        response = client.post("/public-official/create", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

def test_update_public_official_invalid_age(client, auth):
    # Test case: Update a public official with invalid age
    auth.create_admin_user()

    for age in [0, 10, 150, 1000]:
        po_dict_copy = po_dict_template.copy()
        po_dict_copy['age'] = age
        response = client.post("/public-official/create", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

def test_update_public_official_invalid_political_party(client, auth):
    # Test case: Update a public official with invalid political party
    auth.create_admin_user()
    for eng_party in ['', 'מפלגה בעברית']:
        po_dict_copy = po_dict_template.copy()
        po_dict_copy['political_party']['eng'] = eng_party
        response = client.post("/public-official/create", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

    for heb_party in ['', 'english party']:
        po_dict_copy = po_dict_template.copy()
        po_dict_copy['political_party']['heb'] = heb_party
        response = client.post("/public-official/create", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

def test_update_public_official_invalid_social_media_handles(client, auth):
    # Test case: Update a public official with invalid social media handles
    auth.create_admin_user()
    
    po_dict_copy = po_dict_template.copy()
    po_dict_copy['social_media_handles']['fakebook'] = 'myhandle'

    response = client.post("/public-official/create", json=po_dict_copy, headers=auth.get_auth_header())

    assert response.status_code == 400
    
    for social_media_handle in ['', 'with spaces', 'עברית']:
        po_dict_copy = po_dict_template.copy()
        po_dict_copy['social_media_handles']['facebook'] = social_media_handle

        response = client.post("/public-official/create", json=po_dict_copy, headers=auth.get_auth_header())

        assert response.status_code == 400