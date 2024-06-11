from bson import ObjectId
from app.models.publicofficial import PublicOfficial
from app.logic.publicofficial_service import PublicOfficialService
from app.logic.mongo.database import get_po_collection

class PublicOfficialDataManagerMongoDB(PublicOfficialService):
    def __init__(self):
        pass

    def create_public_official(self, public_official: PublicOfficial) -> PublicOfficial:
        inserted_obj = get_po_collection().insert_one(public_official.model_dump(exclude={'id'}))
        public_official.id = inserted_obj.inserted_id
        
        return public_official

    def get_public_official_by_id(self, public_official_id: str) -> PublicOfficial:
        po_dict = get_po_collection().find_one({"_id":ObjectId(public_official_id)})
        public_official = PublicOfficial(**po_dict)

        return public_official

    #TODO this
    def update_public_official(self, public_official_id: str, public_official: PublicOfficial) -> PublicOfficial:
        "Update a PublicOfficial according to the parameters"
        pass

    def get_all_public_officials(self) -> list[PublicOfficial]:
        po_dicts = get_po_collection().find()
        po_list = list()
        
        for po_dict in po_dicts:
            po_list.append(PublicOfficial(**po_dict))
        
        return po_list

    def delete_all_public_officials(self) -> None:
        get_po_collection().delete_many({})