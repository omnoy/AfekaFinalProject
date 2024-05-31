from bson import ObjectId
from typing import Optional, Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, AfterValidator
from app.models.object_id_pydantic_annotation import ObjectIdPydanticAnnotation
from app.models.user_role import UserRole
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str):
    return generate_password_hash(password)

class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]] = Field(default = None,  alias = '_id')
    email: EmailStr
    _password_hash: Annotated[SecretStr, AfterValidator(hash_password)]
    username: Optional[str] = Field(default = None)
    position: Optional[str] = Field(default = None)
    role: UserRole = Field(default = UserRole.BASIC_USER)
    is_authenticated: Optional[bool] = Field(default = True)
    is_active: Optional[bool] = Field(default = True)
    is_anonymous: Optional[bool] = Field(default = False) #users cannot be anonymous

    def get_id(self):
        return str(self.id)
    
    def check_password(self, password: str):
        return check_password_hash(self._password_hash, password)
    
    
