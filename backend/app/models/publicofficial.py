from bson import ObjectId
from typing import Dict, Optional, Annotated
from pydantic import Field, ValidationInfo, field_validator, ValidationError
from app.models.base_class import BaseClass
from app.models.social_media import SocialMedia
from app.models.language import Language, string_language_validator

class PublicOfficial(BaseClass):
    full_name: Dict[str, str] 
    position: Dict[str, str]
    age: Optional[int] = Field(default = None, ge=18, le=120)
    political_party: Optional[Dict[str, str]] = Field(default = None)
    social_media_handles: Optional[dict[SocialMedia, str]] = Field(default = {social_media:None for social_media in SocialMedia})

    @field_validator('full_name', 'position', 'political_party')
    @classmethod
    def string_dict_validator(cls, d: Dict[str, str], info: ValidationInfo):
        assert list(d.keys()) == [l.value for l in Language], f'{info.field_name} must be in English and Hebrew'
        
        allow_numbers = (info.field_name != 'full_name')
        for k, v in d.items():
            assert len(v) >= 3, f'{info.field_name} must be at least 3 characters long'
            assert string_language_validator(v, Language(k), allow_numbers=allow_numbers, allowed_symbols="\'\-\.\" "), f'{info.field_name} must be in {Language(k).get_full_name()} and contain only the following charaters: \'-.\"'
   
        return d
    
    @field_validator('social_media_handles')
    @classmethod
    def social_media_handles_validator(cls, d):
        assert all(social_media_name in SocialMedia for social_media_name in d.keys()), 'Social media handle must be one of the following: ' + ', '.join(SocialMedia)
        for v in d.values():
            assert len(v) > 3, 'Social media handle must be at least 3 characters long'
            assert string_language_validator(v, Language.ENGLISH, allow_numbers=True, allowed_symbols="_\."), 'Social media handle must contain only alphanumeric characters, underscores and periods'

        return d