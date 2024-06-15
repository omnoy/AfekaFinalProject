from bson import ObjectId
from typing import Optional, Annotated
from pydantic import Field, field_validator, ValidationError
from app.models.base_class import BaseClass
from app.models.social_media import SocialMedia

class PublicOfficial(BaseClass):
    name_eng: str = Field(min_length=3)
    name_heb: str = Field(min_length=3)
    position: str = Field(min_length=3)
    political_party: Optional[str] = Field(default = None)
    social_media_handles: Optional[dict[SocialMedia, str]] = Field(default = None)

    @field_validator('name_eng')
    @classmethod
    def name_eng_validator(cls, s):
        assert all(c.isalpha() or c.isspace() for c in s), 'Name must contain only English letters and spaces'
        return s
    
    @field_validator('name_heb')
    @classmethod
    def name_heb_validator(cls, s):
        assert all("\u0590" <= c <= "\u05EA" or c.isspace() or c == "\"" for c in s), 'Name must be in Hebrew (hebrew characters, spaces and quotes only)'
        return s
    
    @field_validator('position')
    @classmethod
    def position_validator(cls, s):
        assert all("\u0590" <= c <= "\u05EA" or c.isspace() or c == "\"" or c.isnumeric() for c in s), 'Position must be in Hebrew (hebrew characters, spaces, quotes and numbers only)'
        return s
    
    @field_validator('social_media_handles')
    @classmethod
    def social_media_handles_validator(cls, d):
        for v in d.values():
            assert len(v) > 3, 'Social media handle must be at least 3 characters long'
            assert all(c.isalnum() or c == '_' for c in v), 'Social media handle must contain only alphanumeric characters and underscores'

        return d