from typing import Dict, List, Optional, Annotated
from pydantic import BaseModel, EmailStr, Field, AfterValidator, StringConstraints, field_validator
from app.models.user_role import UserRole
from app.models.base_class import BaseClass
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(BaseClass):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]
    username: Annotated[str, StringConstraints(min_length=4, pattern=r'^[a-zA-Z0-9]*$')]
    role: UserRole | str = Field(default = UserRole.BASIC_USER)
    favorites: Optional[Dict[str, List[str]]] = Field(default = {'public_official': [], 'generated_post': []})

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
        assert re.match(r'^[a-zA-Z0-9]*$', password_plaintext), 'must be alphanumeric' #validate that password is alphanumeric
        return '__hash__' + generate_password_hash(password_plaintext)

    @field_validator('role')
    @classmethod
    def role_must_be_enum(cls, v):
        if isinstance(v, str):
            assert v in str(UserRole.__members__), 'must be a valid UserRole'
            return UserRole(v)
        else:
            return v
    
    @field_validator('favorites')
    @classmethod
    def favorite_list_validator(cls, d: Dict[str, List[str]]):
        assert set(d) == {'public_official', 'generated_post'}, 'must be favorites of public_official or generated_post'
        
        assert all(isinstance(k, list) for k in d.values()), 'must be a list'
        
        for k in d.keys():
            assert all(ObjectId.is_valid(favorite) for favorite in d[k]), 'must be a list of valid ObjectIds'
        
        return d

    def check_password(self, password_plaintext: str):
        return check_password_hash(self.password.removeprefix('__hash__'), password_plaintext)
    
    def is_admin(self):
        return self.role == UserRole.ADMIN_USER
    
