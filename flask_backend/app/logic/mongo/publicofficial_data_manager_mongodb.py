from bson import ObjectId
from app.extensions import mongo
from app.models.publicofficial import PublicOfficial
from app.logic.publicofficial_service import PublicOfficialService

class PublicOfficialDataManagerMongoDB(PublicOfficialService):
    
    def __init__(self) -> None:
        self.po_collection = mongo.db["public_officials"]

    def create_public_official(self, public_official: PublicOfficial) -> PublicOfficial:
        inserted_obj = self.po_collection.insert_one(public_official.model_dump(exclude={'id'}))
        public_official.id = inserted_obj.inserted_id
        
        return public_official

    def get_public_official_by_id(self, public_official_id: str) -> PublicOfficial:
        po_dict = self.po_collection.find_one({"_id":ObjectId(public_official_id)})
        public_official = PublicOfficial(**po_dict)

        return public_official

    #TODO this
    def update_public_official(self, public_official_id: str, public_official: PublicOfficial) -> PublicOfficial:
        "Update a PublicOfficial according to the parameters"
        pass

    def get_all_public_officials(self) -> list[PublicOfficial]:
        po_dicts = self.po_collection.find()
        po_list = list()
        
        for po_dict in po_dicts:
            po_list.append(PublicOfficial(**po_dict))
        
        return po_list

    def delete_all_public_officials(self) -> None:
        self.po_collection.delete_many({})


#Create Module Level Instance as a Singleton
publicOfficialDataManagerMongo = PublicOfficialDataManagerMongoDB()