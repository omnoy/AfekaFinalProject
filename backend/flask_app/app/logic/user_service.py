from app.models.user import User

class UserService:
    
    def __init__(self) -> None:
        "Initialize User Database"
        pass   

    def create_user(self, user: User) -> User:
        "Create a User for the Database using a User class"
        pass

    def get_user_by_id(self, user_id: str) -> User:
        "Get a User by their ID"
        pass

    def update_user(self, user_id: str, user: User) -> User:
        "Update a User according to the parameters"
        pass

    def get_all_users(self) -> list[User]:
        "Get all users from the database"
        pass

    def delete_all_users(self) -> None:
        "Delete all users from the database"
        pass