import json


def test_get_all_public_officials(client, auth, public_official_actions):
    # Test case: Get all public officials
    auth.create_admin_user()

    po_1 = public_official_actions.create_public_official()
    po_2 = public_official_actions.create_public_official(full_name={"eng": "testman the second", "heb": "טסטמן השני"})
    po_3 = public_official_actions.create_public_official(full_name={"eng": "testman the third", "heb": "טסטמן השלישי"})
    po_list = [po.model_dump() for po in [po_1, po_2, po_3]]
    
    response = client.get("/public-official/all", headers=auth.get_auth_header())

    assert response.status_code == 200

    response_po_list = response.json['public_officials']
    
    assert len(response_po_list) ==  3

    for response_po in response_po_list:
        response_po = dict(response_po)
        assert response_po in po_list

def test_get_all_public_officials_empty(client, auth):
    auth.create_admin_user()
    
    response = client.get("/public-official/all", headers=auth.get_auth_header())

    assert response.status_code == 200

    response_po_list = response.json['public_officials']

    assert len(response_po_list) ==  0
    

def test_get_all_public_officials_basic_user(client, auth):
    auth.create_basic_user()
    
    response = client.get("/public-official/all", headers=auth.get_auth_header())

    assert response.status_code == 200