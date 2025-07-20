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
from src.shared import settings


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

    async def all(
        self,
        odata_options: ODataQueryOptions | None = None,
    ) -> list[Resource]:
        if not odata_options:
            odata_options = ODataQueryOptions(top=settings.MAX_RECORDS_PER_PAGE)

        query = apply_to_sqlalchemy_query(odata_options, SQLiteResourceModel)
        result = await execute(query, SQLiteDBModel)
        resources = result.scalars().all()
        return [
            Resource(
                id=resource.id,
                name=resource.name,
                url=ResourceUrl(value=resource.url),
                type=ResourceType(value=resource.type),
                created_at=resource.created_at.timestamp(),
                updated_at=resource.updated_at.timestamp(),
            )
            for resource in resources
        ]

    async def save(self, resource: Resource) -> Resource:
        resource_model = SQLiteResourceModel(
            name=resource.name,
            url=resource.url.value,
            type=resource.type.value,
        )
        await resource_model.save()
        return Resource(
            id=resource_model.id,
            name=resource_model.name,
            url=ResourceUrl(value=resource_model.url),
            type=ResourceType(value=resource_model.type),
            created_at=resource_model.created_at.timestamp(),
            updated_at=resource_model.updated_at.timestamp(),
        )

    async def delete(self, id_: UUID) -> None:
        resource = await SQLiteResourceModel.get(id_)
        if not resource:
            raise ResourceNotFoundError(id_)
        await resource.delete()
