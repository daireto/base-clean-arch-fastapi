from uuid import UUID

from odata_v4_query import ODataQueryOptions

from src.resources.domain.entities import Resource
from src.resources.domain.errors import ResourceNotFoundError
from src.resources.domain.repositories import ResourceRepositoryABC
from src.shared import settings


class MockResourcesRepository(ResourceRepositoryABC):
    def __init__(self) -> None:
        self.resources = {}

    async def get_by_id(self, id_: UUID) -> Resource:
        if id_ not in self.resources:
            raise ResourceNotFoundError(id_)
        return self.resources[id_]

    async def all(
        self, odata_options: ODataQueryOptions | None = None
    ) -> list[Resource]:
        if not odata_options:
            odata_options = ODataQueryOptions(top=settings.MAX_RECORDS_PER_PAGE)

        if odata_options.skip and odata_options.top:
            return list(self.resources.values())[
                odata_options.skip : odata_options.skip + odata_options.top
            ]

        if odata_options.skip:
            return list(self.resources.values())[odata_options.skip :]

        if odata_options.top:
            return list(self.resources.values())[: odata_options.top]

        return list(self.resources.values())

    async def create(self, resource: Resource) -> Resource:
        self.resources[resource.id] = resource
        return resource

    async def update(self, resource: Resource) -> Resource:
        if resource.id not in self.resources:
            raise ResourceNotFoundError(resource.id)
        self.resources[resource.id] = resource
        return resource

    async def delete(self, id_: UUID) -> None:
        if id_ not in self.resources:
            raise ResourceNotFoundError(id_)
        del self.resources[id_]
