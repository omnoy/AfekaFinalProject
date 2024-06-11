from bson import ObjectId
from typing import Optional, Annotated
from pydantic import Field
from app.models.base_class import BaseClass

class PublicOfficial(BaseClass):
    personal_name: str = Field(default = None)
    position: str = Field(default = None)
    political_party: Optional[str] = Field(default = None)