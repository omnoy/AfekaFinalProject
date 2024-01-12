from bson import json_util, ObjectId
from app.models.user import User

class UserService:
    
    def __init__(self) -> None:
        "Initialize User Database"
        pass   

    def create_user(self, user: User):
        "Create a User for the Database using a User class"
        pass

    def get_user_by_id(self, user_id: str):
        "Get a User by their ID"
        pass

    def update_user(self, user_id: str, user: User):
        "Update a User according to the parameters"
        pass

    def get_all_users(self):
        "Get all users from the database"
        pass

    def delete_all_users(self):
        "Delete all users from the database"
        pass