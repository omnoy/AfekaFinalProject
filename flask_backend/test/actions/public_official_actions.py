from app.logic.mongo.database import get_public_official_collection
from app.models.publicofficial import PublicOfficial

class PublicOfficialActions():
    def __init__(self, client):
        self.client = client

    def create_public_official(self, name_eng="testman", name_heb="טסטמן", position="ראש הטסטים", political_party="טסט פארטי", social_media_handles={"twitter": "testman", "facebook": "testman"}):

        po_dict = {
            "name_eng": name_eng, 
            "name_heb": name_heb, 
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