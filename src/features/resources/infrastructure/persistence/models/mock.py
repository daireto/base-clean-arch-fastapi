import time
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.features.resources.domain.entities import Resource
from src.features.resources.domain.value_objects import ResourceType, ResourceUrl


class MockResourceModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    url: str
    type: str
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)

    def to_entity(self) -> Resource:
        return Resource(
            id=self.id,
            name=self.name,
            url=ResourceUrl(value=self.url),
            type=ResourceType(value=self.type),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, entity: Resource) -> 'MockResourceModel':
        return cls(
            id=entity.id,
            name=entity.name,
            url=entity.url_value,
            type=entity.type_value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
