from bson import ObjectId
from app.models.user import User
from app.logic.user_service import UserService
from app.logic.mongo.database import get_user_collection
from app.models.exceptions.user_already_exists_exception import UserAlreadyExistsException

class UserDataManagerMongoDB(UserService):
    
    def __init__(self):
        pass

    def create_user(self, user: User) -> User:
        if get_user_collection().find_one({"email":user.email}):
            raise UserAlreadyExistsException("User already exists")
        
        inserted_obj = get_user_collection().insert_one(user.model_dump(exclude={'id'}))
        user.id = inserted_obj.inserted_id
        
        return user

    def get_user_by_id(self, user_id: str) -> User:
        user_dict = get_user_collection().find_one({"_id":ObjectId(user_id)})
        if not user_dict:
            return None
        
        user = User(**user_dict)
        return user

    def get_user_by_email(self, user_email: str) -> User:
        user_dict = get_user_collection().find_one({"email":user_email})
        if not user_dict:
            return None
        
        user = User(**user_dict)
        return user

    def update_user(self, user_id: str, user: User) -> User:
        get_user_collection().update_one({"_id":ObjectId(user_id)}, 
                                        user.model_dump(exclude={'id'}))
        return user

    def get_all_users(self) -> list[User]:
        user_dicts = get_user_collection().find()
        user_list = list()
        
        for user_dict in user_dicts:
            user_list.append(User(**user_dict))
        
        return user_list
    
    def delete_all_users(self) -> None:
        get_user_collection().delete_many({})