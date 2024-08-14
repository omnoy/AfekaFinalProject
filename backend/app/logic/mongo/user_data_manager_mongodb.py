from typing import List
from bson import ObjectId
from app.models.user import User
from app.logic.user_service import UserService
from app.logic.mongo.database import get_user_collection
from app.models.exceptions.object_already_exists_exception import ObjectAlreadyExistsException
from app.models.exceptions.object_id_not_found_exception import ObjectIDNotFoundException

class UserDataManagerMongoDB(UserService):
    
    def __init__(self):
        pass

    def create_user(self, user: User) -> User:
        if get_user_collection().find_one({"email":user.email}):
            raise ObjectAlreadyExistsException("User already exists")
        
        for favorite_type in ['public_official', 'generated_post']:
            if favorite_type not in user.favorites.keys():
                user.favorites[favorite_type] = []
        
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
        "Updates User according to the parameters. Returns User if successful, None otherwise."
        result = get_user_collection().update_one({"_id":ObjectId(user_id)}, 
                                            {"$set":user.model_dump(exclude={'id'})})
        if result.matched_count == 0:
            return None
        
        return user
    
    def get_favorite_ids(self, favorite_type: str, user_id: str) -> List[str]:
        user_dict = get_user_collection().find_one({"_id":ObjectId(user_id)})
        if not user_dict:
            raise ObjectIDNotFoundException(f"User {user_id} not found")
        
        if favorite_type not in user_dict["favorites"].keys():
            return []
        
        return sorted(user_dict["favorites"][favorite_type], reverse=True) #sort favorites by creation date embedded into the id
    
    def add_favorite(self, favorite_type: str, user_id: str, object_id: str) -> None:
        if favorite_type not in ['public_official', 'generated_post']:
            raise KeyError("Invalid favorite type")
        
        favorites = get_user_collection().find_one({"_id":ObjectId(user_id)})["favorites"]

        if favorite_type not in favorites.keys() or object_id not in favorites[favorite_type]:
            result = get_user_collection().update_one({"_id":ObjectId(user_id)}, 
                                                {"$push":{f"favorites.{favorite_type}":object_id}}, upsert=True)
            if result.matched_count == 0:
                raise Exception(f"Adding favorite {object_id} to {user_id} failed") #should not be here


    def remove_favorite(self, favorite_type: str, user_id: str, object_id: str) -> None:
        if favorite_type not in ['public_official', 'generated_post']:
            raise KeyError("Invalid favorite type")
        
        favorites = get_user_collection().find_one({"_id":ObjectId(user_id)})["favorites"]

        if favorite_type in favorites.keys() and object_id in favorites[favorite_type]:
            result = get_user_collection().update_one({"_id":ObjectId(user_id)}, 
                                                {"$pull":{f"favorites.{favorite_type}":object_id}}, upsert=True)
            if result.matched_count == 0:
                raise Exception(f"Removing favorite {object_id} to {user_id} failed") #should not be here
        else:
            raise ObjectIDNotFoundException(f"Favorite {favorite_type} id not in user favorites")
    
    def get_all_users(self) -> list[User]:
        user_dicts = get_user_collection().find()
        user_list = list()
        
        for user_dict in user_dicts:
            user_list.append(User(**user_dict))
        
        return user_list
    
    def delete_all_users(self) -> None:
        get_user_collection().delete_many({})