from bson import ObjectId
from app.extensions import mongo
from app.models.user import User
from app.logic.user_service import UserService
from app.extensions import login_manager

class UserDataManagerMongoDB(UserService):
    
    def __init__(self) -> None:
        self.user_collection = mongo.db["users"]    

    def create_user(self, user: User) -> User:
        if self.user_collection.collection.count_documents({ 'email': user.email }, limit = 1):
            raise Exception("User already exists")
        
        inserted_obj = self.user_collection.insert_one(user.model_dump(exclude={'id'}))
        user.id = inserted_obj.inserted_id
        
        return user

    def get_user_by_id(self, user_id: str) -> User:
        user_dict = self.user_collection.find_one({"_id":ObjectId(user_id)})
        user = User(**user_dict)

        return user

    def get_user_by_email(self, user_email: str) -> User:
        user_dict = self.user_collection.find_one({"email":user_email})
        user = User(**user_dict)

        return user

    def update_user(self, user_id: str, user: User) -> User:
        self.user_collection.update_one({"_id":ObjectId(user_id)}, 
                                        user.model_dump(exclude={'id'}))
        return user

    def get_all_users(self) -> list[User]:
        user_dicts = self.user_collection.find()
        user_list = list()
        
        for user_dict in user_dicts:
            user_list.append(User(**user_dict))
        
        return user_list
    
    def delete_all_users(self) -> None:
        self.user_collection.delete_many({})


#Create Module Level Instance as a Singleton
userDataManagerMongoDB = UserDataManagerMongoDB()