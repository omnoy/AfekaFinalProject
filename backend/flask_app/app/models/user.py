from bson import ObjectId
from typing import Optional, Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.object_id_pydantic_annotation import ObjectIdPydanticAnnotation
from app.models.user_role import UserRole

class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]] = Field(default = None,  alias = '_id')
    username: str = Field(min_length=1)
    personal_name: Optional[str] = Field(default = None)
    email: EmailStr
    position: Optional[str] = Field(default = None)
    role: UserRole = Field(default = UserRole.BASIC_USER)