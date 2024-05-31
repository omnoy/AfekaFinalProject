from bson import ObjectId
from typing import Optional, Annotated
from pydantic import BaseModel, ConfigDict, Field

from app.models.object_id_pydantic_annotation import ObjectIdPydanticAnnotation
from datetime import datetime

class PublicOfficial(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]] = Field(default = None,  alias = '_id')
    personal_name: str = Field(default = None)
    position: str = Field(default = None)
    political_party: Optional[str] = Field(default = None)