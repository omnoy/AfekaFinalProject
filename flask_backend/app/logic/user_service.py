from abc import ABC, abstractmethod
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
    def get_all_users(self) -> list[User]:
        "Get all users from the database"
        pass

    @abstractmethod
    def delete_all_users(self) -> None:
        "Delete all users from the database"
        pass