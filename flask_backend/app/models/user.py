from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, Field, AfterValidator, field_validator
from app.models.user_role import UserRole
from app.models.base_class import BaseClass
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import logger

class User(BaseClass):
    email: EmailStr
    password: str = Field(min_length=8, description='Password must be at least 8 characters long.')
    username: str = Field(min_length=5)
    position: Optional[str] = Field(default = None, min_length=5)
    role: UserRole = Field(default = UserRole.BASIC_USER)
    
    @field_validator('username')
    @classmethod
    def name_must_be_alphanumeric(cls, v: str) -> str:
        assert v.isalnum(), 'must be alphanumeric'
        return v
    

    @field_validator('password')
    @classmethod
    def hash_password(cls, password_plaintext: str) -> str:
        if password_plaintext.startswith('__hash__'):
            return password_plaintext #password is already hashed
        
        assert password_plaintext.isalnum(), 'must be alphanumeric' #validate that password is alphanumeric

        return '__hash__' + generate_password_hash(password_plaintext)

    @field_validator('position')
    @classmethod
    def position_must_be_alpha(cls, v: str):
        if isinstance(v, str):
            assert all(c.isalnum() or c.isspace() for c in v), 'must be alphabetic'
        return v
    
    def check_password(self, password_plaintext: str):
        return check_password_hash(self.password.removeprefix('__hash__'), password_plaintext)
    
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
