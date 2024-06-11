from bson import ObjectId
from typing import Optional, Annotated
from pydantic import Field
from app.models.object_id_pydantic_annotation import ObjectIdPydanticAnnotation
from app.models.social_media import SocialMedia
from app.models.base_class import BaseClass

class GeneratedPost(BaseClass):
    user_id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]] = Field(default = None)
    public_official_id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(default = None)
    title: str = Field(default="Untitled Post", min_length=1)
    text: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    social_media: Optional[SocialMedia]