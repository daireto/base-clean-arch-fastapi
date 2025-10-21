from uuid import UUID

from sqlactive import ActiveRecordBaseModel
from sqlalchemy.orm import Mapped, mapped_column

from src.features.resources.domain.entities import Resource
from src.features.resources.domain.value_objects import ResourceType, ResourceUrl


class SQLiteResourcesBaseModel(ActiveRecordBaseModel):
    __abstract__ = True


class SQLiteResourceModel(SQLiteResourcesBaseModel):
    __tablename__ = 'resources'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()

    def to_entity(self) -> 'Resource':
        return Resource(
            id=self.id,
            name=self.name,
            url=ResourceUrl(value=self.url),
            type=ResourceType(value=self.type),
            created_at=self.created_at.timestamp(),
            updated_at=self.updated_at.timestamp(),
        )

    @classmethod
    def from_entity(cls, entity: 'Resource') -> 'SQLiteResourceModel':
        return cls(
            id=entity.id,
            name=entity.name,
            url=entity.url_value,
            type=entity.type_value,
        )
