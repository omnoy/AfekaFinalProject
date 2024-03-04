from bson import ObjectId
from typing import Optional, Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.object_id_pydantic_annotation import ObjectIdPydanticAnnotation
from app.models.social_media import SocialMedia

class GeneratedPost(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]] = Field(default = None,  alias = '_id')
    user_id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]] = Field(default = None)
    public_official_id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(default = None)
    prompt: str = Field(min_length=1)
    title: str = Field(default="Untitled Post", min_length=1)
    text: str = Field(min_length=1)
    social_media: Optional[SocialMedia]