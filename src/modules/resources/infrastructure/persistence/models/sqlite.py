from uuid import UUID, uuid4

from sqlactive import ActiveRecordBaseModel
from sqlalchemy.orm import Mapped, mapped_column

from modules.resources.domain.entities import Resource
from modules.resources.domain.value_objects import ResourceType, ResourceUrl


class BaseModel(ActiveRecordBaseModel):
    __abstract__ = True


class ResourceModel(BaseModel):
    __tablename__ = 'resources'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()

    def to_entity(self) -> Resource:
        return Resource(
            id=self.id,
            name=self.name,
            url=ResourceUrl(value=self.url),
            type=ResourceType(value=self.type),
            created_at=self.created_at.timestamp(),
            updated_at=self.updated_at.timestamp(),
        )

    @classmethod
    def from_entity(cls, entity: Resource) -> 'ResourceModel':
        return cls(
            id=entity.id,
            name=entity.name,
            url=entity.url_value,
            type=entity.type_value,
        )
