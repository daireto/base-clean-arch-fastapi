from sqlalchemy import create_engine
from sqlmodel import Field, Session, SQLModel, select

from resources.domain.models import Resource
from resources.domain.repositories import ResourcesRepository
from resources.domain.value_objects import ResourceUrl


class ResourceModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str


engine = create_engine('sqlite:///database.db')
SQLModel.metadata.create_all(engine)


class SQLModelResourcesRepository(ResourcesRepository):
    def all(self) -> list[Resource]:
        with Session(engine) as session:
            resources = session.exec(select(ResourceModel)).all()

        return [Resource(ResourceUrl(value=resource.url)) for resource in resources]

    def save(self, resource: Resource) -> None:
        resource_model = ResourceModel(url=resource.url.value)
        with Session(engine) as session:
            session.add(resource_model)
            session.commit()
