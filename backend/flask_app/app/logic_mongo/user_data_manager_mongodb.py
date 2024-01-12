from bson import json_util, ObjectId
from app.extensions import mongo
from app.models.user import User
from app.logic.user_service import UserService

class UserDataManagerMongoDB(UserService):
    
    def __init__(self) -> None:
        self.user_collection = mongo.db["users"]    

    def create_user(self, user: User):
        inserted_obj = self.user_collection.insert_one(user.__dict__)

        return inserted_obj._id

    def get_user_by_id(self, user_id: str):
        return json_util.dumps(self.user_collection.find_one({"_id":ObjectId(user_id)}))

    def update_user(self, user_id: str):
        pass

    def get_all_users(self):
        return json_util.dumps(self.user_collection.find())
    
    def delete_all_users(self):
        pass