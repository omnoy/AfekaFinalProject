from pydantic import BaseModel, ConfigDict, Field, field_serializer
from typing import Optional, Annotated
from bson import ObjectId
from abc import ABC
from app.models.object_id_pydantic_annotation import ObjectIdPydanticAnnotation

class BaseClass(BaseModel, ABC):
    model_config = ConfigDict(
        populate_by_name=True, 
        extra='forbid',
        revalidate_instances='always',
        validate_assignment=True)
    id: Optional[Annotated[ObjectId, ObjectIdPydanticAnnotation]] = Field(default = None,  alias = '_id')

    def get_id(self) -> str:
        '''Returns string of Mongos ObjectID'''
        return str(self.id)
    
    @field_serializer('id')
    def serialize_id(self, id: ObjectId) -> str:
        '''Returns string of Mongos ObjectID'''
        return str(id)