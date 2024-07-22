from app.logic.mongo.database import get_public_official_collection
from app.models.publicofficial import PublicOfficial

class PublicOfficialActions():
    def __init__(self, client):
        self.client = client

    def create_public_official(self, 
                               full_name={"eng": "testman", "heb": "טסטמן"}, 
                               age=30,
                               position= {"eng": "Lead Tester", "heb": "ראש הטסטים"}, 
                               political_party={"eng": "Test Party", "heb": "טסט פארטי"}, 
                               social_media_handles={"twitter": "testman", "facebook": "testman"}):
        po_dict = {
            "full_name": full_name,
            "age": age,
            "position": position,
            "political_party": political_party,
            "social_media_handles": social_media_handles
        }

        inserted_obj = get_public_official_collection().insert_one(po_dict)
        
        po_dict["_id"] = inserted_obj.inserted_id
        self.public_official = PublicOfficial(**po_dict)
        return self.public_official
    
    def get_public_official_id(self) -> str:
        return self.public_official.get_id()