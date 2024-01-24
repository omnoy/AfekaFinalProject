from bson import ObjectId
from typing import Optional, Annotated
from pydantic import BaseModel, Field

from app.models.object_id_pydantic_annotation import ObjectIdPydanticAnnotation
from app.models.social_media import SocialMedia

class GenerationPrompt(BaseModel):
    title: str = Field(default="Untitled Post", min_length=1)
    user_id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]] = Field(default = None)
    public_official_id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(default = None)
    prompt: str = Field(min_length=1)
    parameters: Optional[dict]
    social_media: Optional[SocialMedia]