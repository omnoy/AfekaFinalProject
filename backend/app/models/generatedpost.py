from bson import ObjectId
from typing import Optional, Annotated
from pydantic import Field, field_serializer
from app.models.object_id_pydantic_annotation import ObjectIdPydanticAnnotation
from app.models.social_media import SocialMedia
from app.models.base_class import BaseClass

class GeneratedPost(BaseClass): # GeneratedPost is a pydantic model to validate potential invalid model output
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(default = None)
    public_official_id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(default = None)
    title: str = Field(default="Untitled Post", min_length=1)
    text: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    social_media: Optional[SocialMedia]

    @field_serializer('user_id', 'public_official_id')
    def serialize_object_id(self, id: ObjectId) -> str:
        '''Returns string of Mongos ObjectID'''
        return str(id)