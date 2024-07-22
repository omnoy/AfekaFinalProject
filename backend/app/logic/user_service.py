from abc import ABC, abstractmethod
from typing import List
from app.models.user import User

class UserService(ABC):
    
    @abstractmethod
    def __init__(self) -> None:
        "Initialize User Database"
        pass   
    
    @abstractmethod
    def create_user(self, user: User) -> User:
        "Create a User for the Database using a User class"
        pass

    @abstractmethod
    def get_user_by_email(self, user_email: str) -> User:
        "Get a User by their email"
        pass

    @abstractmethod
    def update_user(self, user_id: str, user: User) -> User:
        "Update a User according to the parameters"
        pass

    @abstractmethod
    def get_favorite_ids(self, favorite_type: str, user_id: str) -> List[str]:
        "Get a list of favorite public_officials or generated_posts from a User"
        pass

    @abstractmethod
    def add_favorite(self, favorite_type: str, user_id: str, object_id: str) -> None:
        "Add a favorite public_official or generated_post to a User"
        pass

    @abstractmethod
    def remove_favorite(self, favorite_type: str, user_id: str, object_id: str) -> None:
        "Remove a favorite public_official or generated_post from a User"
        pass

    @abstractmethod
    def get_all_users(self) -> list[User]:
        "Get all users from the database"
        pass

    @abstractmethod
    def delete_all_users(self) -> None:
        "Delete all users from the database"
        pass