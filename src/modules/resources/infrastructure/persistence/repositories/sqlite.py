from uuid import UUID

from odata_v4_query import ODataQueryOptions
from odata_v4_query.utils.sqlalchemy import apply_to_sqlalchemy_query
from sqlactive import execute

from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.infrastructure.persistence.models.sqlite import (
    SQLiteResourceModel,
    SQLiteResourcesBaseModel,
)


class SQLiteResourceRepository(ResourceRepositoryABC):
    async def get_by_id(self, id_: UUID) -> Resource | None:
        resource = await SQLiteResourceModel.get(id_)
        return resource.to_entity() if resource else None

    async def all(self, odata_options: ODataQueryOptions) -> list[Resource]:
        query = apply_to_sqlalchemy_query(odata_options, SQLiteResourceModel)
        result = await execute(query, SQLiteResourcesBaseModel)
        resources = result.scalars().all()
        return [resource.to_entity() for resource in resources]

    async def create(self, resource: Resource) -> Resource:
        model = SQLiteResourceModel.from_entity(resource)
        await model.save()
        return model.to_entity()

    async def update(self, resource: Resource) -> Resource | None:
        model = await SQLiteResourceModel.get(resource.id)
        if not model:
            return None
        model.name = resource.name
        model.url = resource.url_value
        model.type = resource.type_value
        await model.save()
        return model.to_entity()

    async def delete(self, id_: UUID) -> bool:
        resource = await SQLiteResourceModel.get(id_)
        if not resource:
            return False
        await resource.delete()
        return True

    async def count(self, odata_options: ODataQueryOptions | None = None) -> int:
        if odata_options:
            query = apply_to_sqlalchemy_query(odata_options, SQLiteResourceModel)
            result = await execute(query, SQLiteResourcesBaseModel)
            return result.scalar_one()
        return await SQLiteResourceModel.count()
