import json

from bson import ObjectId
from app.logic.mongo.database import get_public_official_collection

def test_update_public_official(client, auth, public_official_actions):
    # Test case: Update a public official with valid data
    auth.create_admin_user()

    public_official = public_official_actions.create_public_official()
    po_dict = public_official.model_dump()

    po_dict['full_name']['eng'] = 'new name'
    po_dict['full_name']['heb'] = 'שם חדש'

    response = client.put(f"/public-official/update/{public_official.get_id()}", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 200

    response_po_dict = response.json['public_official']
    assert response_po_dict == po_dict

    db_po_dict = get_public_official_collection().find_one({"_id": ObjectId(public_official.get_id())})
    db_po_dict['id'] = str(db_po_dict['_id'])
    db_po_dict.pop('_id')
    
    assert db_po_dict == po_dict

def test_update_public_official_unauthorized(client, auth, public_official_actions):
    auth.create_basic_user()
    
    public_official_actions.create_public_official()
    
    response = client.put(f"/public-official/update/{public_official_actions.get_public_official_id()}", json={}, headers=auth.get_auth_header())
    
    assert response.status_code == 401

def test_update_public_official_invalid_id(client, auth, public_official_actions):
    # Test case: Update a public official with an invalid public official ID given
    auth.create_admin_user()

    public_official = public_official_actions.create_public_official()
    po_dict = public_official.model_dump()
    po_dict.pop('id')
    
    response = client.put(f"/public-official/update/666d7c070477c0def6d136c9", json=po_dict, headers=auth.get_auth_header())

    assert response.status_code == 404

def test_update_public_official_invalid_full_name(client, auth, public_official_actions):
    # Test case: Update a public official with invalid full name
    auth.create_admin_user()

    public_official = public_official_actions.create_public_official()
    po_dict = public_official.model_dump()

    for eng_name in ['123', '', 'שם בעברית', 'שם בעברית123']:
        po_dict_copy = po_dict.copy()
        po_dict_copy['full_name']['eng'] = eng_name
        response = client.put(f"/public-official/update/{public_official.get_id()}", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

    for heb_name in ['123', '', 'english name', 'english name123']:
        po_dict_copy = po_dict.copy()
        po_dict_copy['full_name']['heb'] = heb_name
        response = client.put(f"/public-official/update/{public_official.get_id()}", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

def test_update_public_official_invalid_position(client, auth, public_official_actions):
    # Test case: Update a public official with invalid position
    auth.create_admin_user()

    public_official = public_official_actions.create_public_official()
    po_dict = public_official.model_dump()

    for eng_position in ['', 'תפקיד בעברית']:
        po_dict_copy = po_dict.copy()
        po_dict_copy['position']['eng'] = eng_position
        response = client.put(f"/public-official/update/{public_official.get_id()}", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

    for heb_position in ['', 'english position']:
        po_dict_copy = po_dict.copy()
        po_dict_copy['position']['heb'] = heb_position
        response = client.put(f"/public-official/update/{public_official.get_id()}", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

def test_update_public_official_invalid_age(client, auth, public_official_actions):
    # Test case: Update a public official with invalid age
    auth.create_admin_user()

    public_official = public_official_actions.create_public_official()
    po_dict = public_official.model_dump()

    for age in [0, 10, 150, 1000]:
        po_dict_copy = po_dict.copy()
        po_dict_copy['age'] = age
        response = client.put(f"/public-official/update/{public_official.get_id()}", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

def test_update_public_official_invalid_political_party(client, auth, public_official_actions):
    # Test case: Update a public official with invalid political party
    auth.create_admin_user()

    public_official = public_official_actions.create_public_official()
    po_dict = public_official.model_dump()

    for eng_party in ['', 'מפלגה בעברית']:
        po_dict_copy = po_dict.copy()
        po_dict_copy['political_party']['eng'] = eng_party
        response = client.put(f"/public-official/update/{public_official.get_id()}", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

    for heb_party in ['', 'english party']:
        po_dict_copy = po_dict.copy()
        po_dict_copy['political_party']['heb'] = heb_party
        response = client.put(f"/public-official/update/{public_official.get_id()}", json=po_dict_copy, headers=auth.get_auth_header())
        assert response.status_code == 400

def test_update_public_official_invalid_social_media_handles(client, auth, public_official_actions):
    # Test case: Update a public official with invalid social media handles
    auth.create_admin_user()

    public_official = public_official_actions.create_public_official()
    po_dict = public_official.model_dump()
    po_dict_copy = po_dict.copy()
    po_dict_copy['social_media_handles']['fakebook'] = 'myhandle'

    response = client.put(f"/public-official/update/{public_official.get_id()}", json=po_dict_copy, headers=auth.get_auth_header())

    assert response.status_code == 400
    
    for social_media_handle in ['', 'with spaces', 'עברית']:
        po_dict_copy = po_dict.copy()
        po_dict_copy['social_media_handles']['facebook'] = social_media_handle

        response = client.put(f"/public-official/update/{public_official.get_id()}", json=po_dict_copy, headers=auth.get_auth_header())

        assert response.status_code == 400
    