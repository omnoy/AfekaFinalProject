from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, Field, AfterValidator
from app.models.user_role import UserRole
from app.models.base_class import BaseClass
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password_plaintext: str) -> str:
    if password_plaintext.startswith('__hash__'):
        return password_plaintext #password is already hashed

    return '__hash__' + generate_password_hash(password_plaintext)

class User(BaseClass):
    email: EmailStr
    password_hash: Annotated[str, AfterValidator(hash_password)] = Field(alias = 'password')
    username: Optional[str] = Field(default = None)
    position: Optional[str] = Field(default = None)
    role: UserRole = Field(default = UserRole.BASIC_USER)
    is_authenticated: Optional[bool] = Field(default = True)
    is_active: Optional[bool] = Field(default = True)
    is_anonymous: Optional[bool] = Field(default = False) #users cannot be anonymous
    
    def check_password(self, password_plaintext: str):
        return check_password_hash(self.password_hash.removeprefix('__hash__'), password_plaintext)
    
    
