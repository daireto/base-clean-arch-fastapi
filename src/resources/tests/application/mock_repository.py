from uuid import UUID

from src.resources.domain.entities import Resource
from src.resources.domain.errors import ResourceNotFoundError
from src.resources.domain.repositories import ResourceRepositoryABC


class MockResourcesRepository(ResourceRepositoryABC):
    def __init__(self) -> None:
        self.resources = {}

    async def get_by_id(self, id_: UUID) -> Resource:
        if id_ not in self.resources:
            raise ResourceNotFoundError(id_)
        return self.resources[id_]

    async def all(self) -> list[Resource]:
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
