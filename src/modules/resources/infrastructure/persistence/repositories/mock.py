from uuid import UUID

from odata_v4_query import ODataQueryOptions

from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.infrastructure.persistence.models.mock import (
    MockResourceModel,
)


class MockResourceRepository(ResourceRepositoryABC):
    def __init__(self) -> None:
        self._storage: dict[UUID, MockResourceModel] = {}

    async def get_by_id(self, id_: UUID) -> Resource | None:
        resource = self._storage.get(id_)
        return resource.to_entity() if resource else None

    async def all(self, odata_options: ODataQueryOptions) -> list[Resource]:
        resources = list(self._storage.values())
        if odata_options.skip:
            resources = resources[odata_options.skip :]
        if odata_options.top:
            resources = resources[: odata_options.top]
        return [model.to_entity() for model in resources]

    async def create(self, resource: Resource) -> Resource:
        model = MockResourceModel.from_entity(resource)
        self._storage[model.id] = model
        return model.to_entity()

    async def update(self, resource: Resource) -> Resource | None:
        model = self._storage.get(resource.id)
        if not model:
            return None
        model = MockResourceModel.from_entity(resource)
        self._storage[resource.id] = model
        model.id = resource.id
        return model.to_entity()

    async def delete(self, id_: UUID) -> bool:
        resource = self._storage.get(id_)
        if not resource:
            return False
        del self._storage[id_]
        return True

    async def count(self, _: ODataQueryOptions | None = None) -> int:
        return len(self._storage)
