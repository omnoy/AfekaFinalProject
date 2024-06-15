from app.logic.mongo.database import get_public_official_collection

def test_delete_all_public_officials(client, auth):
    auth.create_admin()

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

    response = client.delete("/public-official/all", headers=auth.get_auth_header())

    assert response.status_code == 200

    assert len(list(get_public_official_collection().find({}))) == 0

def test_delete_all_public_officials_invalid_auth(client, auth):
    auth.create_admin()

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
    
    auth.create_basic_user()

    response = client.delete("/public-official/all", headers=auth.get_auth_header())

    assert response.status_code == 403

    assert len(list(get_public_official_collection().find({}))) == 3