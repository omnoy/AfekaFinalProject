from bson import ObjectId
from app.models.publicofficial import PublicOfficial
from app.logic.publicofficial_service import PublicOfficialService
from app.logic.mongo.database import get_public_official_collection

class PublicOfficialDataManagerMongoDB(PublicOfficialService):
    def __init__(self):
        pass

    def create_public_official(self, public_official: PublicOfficial) -> PublicOfficial:
        inserted_obj = get_public_official_collection().insert_one(public_official.model_dump(exclude={'id'}))

        public_official.id = inserted_obj.inserted_id
        
        return public_official

    def get_public_official_by_id(self, public_official_id: str) -> PublicOfficial:
        po_dict = get_public_official_collection().find_one({"_id":ObjectId(public_official_id)})
        if not po_dict:
            return None
        
        public_official = PublicOfficial(**po_dict)

        return public_official
    
    def get_public_official_by_id_list(self, public_official_id_list: list[str]) -> list[PublicOfficial]:
        po_dicts = get_public_official_collection().find({"_id": {"$in": [ObjectId(po_id) for po_id in public_official_id_list]}}).sort([['_id', -1]])
        po_list = list()
        
        for po_dict in po_dicts:
            po_list.append(PublicOfficial(**po_dict))
        
        return po_list

    def update_public_official(self, public_official_id: str, public_official: PublicOfficial) -> PublicOfficial:
        "Update a PublicOfficial according to the parameters"
        
        result = get_public_official_collection().update_one({"_id":ObjectId(public_official_id)}, 
                                        {"$set":public_official.model_dump(exclude={'id'})})
        if result.matched_count == 0:
            return None
        
        return public_official

    def get_all_public_officials(self) -> list[PublicOfficial]:
        po_dicts = get_public_official_collection().find({}).sort([['_id', -1]])
        po_list = list()
        
        for po_dict in po_dicts:
            po_list.append(PublicOfficial(**po_dict))
        
        return po_list

    def delete_all_public_officials(self) -> None:
        get_public_official_collection().delete_many({})