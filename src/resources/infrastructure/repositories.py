from uuid import UUID

from odata_v4_query import ODataQueryOptions
from odata_v4_query.utils.sqlalchemy import apply_to_sqlalchemy_query
from sqlactive import execute

from resources.domain.entities import Resource
from resources.domain.errors import ResourceNotFoundError
from resources.domain.repositories import ResourceRepositoryABC
from resources.domain.value_objects import ResourceType, ResourceUrl
from resources.infrastructure.models import DBModel, SQLiteResourceModel


class SQLiteResourceRepository(ResourceRepositoryABC):
    async def get_by_id(self, id_: UUID) -> Resource:
        resource = await SQLiteResourceModel.get(id_)
        if not resource:
            raise ResourceNotFoundError(id_)

        return Resource(
            id=resource.id,
            name=resource.name,
            url=ResourceUrl(value=resource.url),
            type=ResourceType(value=resource.type),
            created_at=resource.created_at.timestamp(),
            updated_at=resource.updated_at.timestamp(),
        )

    async def all(self, odata_options: ODataQueryOptions) -> list[Resource]:
        query = apply_to_sqlalchemy_query(odata_options, SQLiteResourceModel)
        result = await execute(query, DBModel)
        resources = result.scalars().all()
        return [
            Resource(
                id=resource.pk,
                name=resource.name,
                url=ResourceUrl(value=resource.url),
                type=ResourceType(value=resource.type),
                created_at=resource.created_at.timestamp(),
                updated_at=resource.updated_at.timestamp(),
            )
            for resource in resources
        ]

    async def save(self, resource: Resource) -> SQLiteResourceModel:
        resource_model = SQLiteResourceModel(
            name=resource.name,
            url=resource.url.value,
            type=resource.type,
        )
        return await resource_model.save()
