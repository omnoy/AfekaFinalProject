from bson import ObjectId
from typing import Optional, Annotated
from pydantic import Field, field_serializer, field_validator
from app.models.object_id_pydantic_annotation import ObjectIdPydanticAnnotation
from app.models.social_media import SocialMedia
from app.models.base_class import BaseClass
from app.models.language import Language

class GeneratedPost(BaseClass): # GeneratedPost is a pydantic model to validate potential invalid model output
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(default = None)
    public_official_id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(default = None)
    title: str = Field(default="Untitled Post", min_length=1)
    text: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    language: Language | str
    social_media: SocialMedia | str

    @field_serializer('user_id', 'public_official_id')
    def serialize_object_id(self, id: ObjectId) -> str:
        '''Returns string of Mongos ObjectID'''
        return str(id)

    @field_validator('language')
    @classmethod
    def language_must_be_enum(cls, v):
        if isinstance(v, str):
            assert v in str(Language.__members__), 'must be a valid Language'
            return Language(v)
        else:
            return v
    
    @field_validator('social_media')
    @classmethod
    def social_media_must_be_enum(cls, v):
        if isinstance(v, str):
            assert v in str(SocialMedia.__members__), 'must be a valid SocialMedia'
            return SocialMedia(v)
        else:
            return v