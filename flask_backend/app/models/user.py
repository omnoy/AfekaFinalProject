from typing import Dict, List, Optional, Annotated
from pydantic import BaseModel, EmailStr, Field, AfterValidator, field_validator
from app.models.user_role import UserRole
from app.models.base_class import BaseClass
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseClass):
    email: EmailStr
    password: str = Field(min_length=8, description='Password must be at least 8 characters long.')
    username: str = Field(min_length=5)
    position: Optional[str] = Field(default = None, min_length=5)
    role: UserRole = Field(default = UserRole.BASIC_USER)
    favorites: Dict[str, List[str]] = Field(default = {})

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
    
    @field_validator('favorites')
    @classmethod
    def favorite_list_validator(cls, d: Dict[str, List[str]]):
        assert all(k in ['public_official', 'generated_post'] for k in d.keys()), 'must be favorites of public_official or generated_post'
        
        for k in d.keys():
            assert all(ObjectId.is_valid(favorite) for favorite in d[k]), 'must be a list of valid ObjectIds'
        
        return d

    def check_password(self, password_plaintext: str):
        return check_password_hash(self.password.removeprefix('__hash__'), password_plaintext)
    
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
