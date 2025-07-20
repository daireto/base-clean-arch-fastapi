from uuid import UUID

from odata_v4_query import ODataQueryOptions
from odata_v4_query.utils.sqlalchemy import apply_to_sqlalchemy_query
from sqlactive import execute

from src.resources.domain.entities import Resource
from src.resources.domain.errors import ResourceNotFoundError
from src.resources.domain.repositories import ResourceRepositoryABC
from src.resources.domain.value_objects import ResourceType, ResourceUrl
from src.resources.infrastructure.models.sqlite import (
    SQLiteDBModel,
    SQLiteResourceModel,
)


class SQLiteResourceRepository(ResourceRepositoryABC):
    async def get_by_id(self, id_: UUID) -> Resource:
        resource = await SQLiteResourceModel.get(id_)
        if not resource:
            raise ResourceNotFoundError(id_)

        return self.__get_model_to_entity(resource)

    async def all(self, odata_options: ODataQueryOptions) -> list[Resource]:
        query = apply_to_sqlalchemy_query(odata_options, SQLiteResourceModel)
        result = await execute(query, SQLiteDBModel)
        resources = result.scalars().all()
        return [self.__get_model_to_entity(resource) for resource in resources]

    async def create(self, resource: Resource) -> Resource:
        resource_model = SQLiteResourceModel(
            name=resource.name,
            url=resource.url.value,
            type=resource.type.value,
        )
        await resource_model.save()
        return self.__get_model_to_entity(resource_model)

    async def update(self, resource: Resource) -> Resource:
        resource_model = await SQLiteResourceModel.get(resource.id)
        if not resource_model:
            raise ResourceNotFoundError(resource.id)

        resource_model.name = resource.name
        resource_model.url = resource.url.value
        resource_model.type = resource.type.value
        await resource_model.save()
        return self.__get_model_to_entity(resource_model)

    async def delete(self, id_: UUID) -> None:
        resource = await SQLiteResourceModel.get(id_)
        if not resource:
            raise ResourceNotFoundError(id_)
        await resource.delete()

    def __get_model_to_entity(self, model: SQLiteResourceModel) -> Resource:
        return Resource(
            id=model.id,
            name=model.name,
            url=ResourceUrl(value=model.url),
            type=ResourceType(value=model.type),
            created_at=model.created_at.timestamp(),
            updated_at=model.updated_at.timestamp(),
        )
