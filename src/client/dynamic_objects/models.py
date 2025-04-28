from typing import List, Optional

from pydantic import BaseModel, Field

from ..shared_models import Links


class Domain(BaseModel):
    id: str
    type: str
    name: str


class LastUser(BaseModel):
    name: str
    id: str
    type: str


class DynamicObjectMetadata(BaseModel):
    domain: Domain
    lastUser: LastUser


class NewDynamicObject(BaseModel):
    name: str
    description: Optional[str] = None
    type: str = "DynamicObject"
    objectType: str = "IP"
    agentId: str = "CSDACLite"
    topicName: str = "CSDACLite"

    def __str__(self) -> str:
        return f"NewDynamicObject(name={self.name}, description={self.description}, type={self.type}, objectType={self.objectType}, agentId={self.agentId}, topicName={self.topicName})"


class DynamicObject(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    type: str
    objectType: str
    agentId: Optional[str] = None
    topicName: Optional[str] = None
    metadata: Optional[DynamicObjectMetadata] = None
    links: Links


class DynamicObjectCollection(BaseModel):
    links: Links
    items: List[DynamicObject] = Field(default_factory=list)


class DynamicMapping(BaseModel):
    mapping: str


class DynamicMappingCollection(BaseModel):
    items: List[DynamicMapping] = Field(default_factory=list)
