from dataclasses import dataclass
from uuid import UUID

from src.resources.domain.entities import Resource
from src.resources.domain.repositories import ResourceRepositoryABC
from src.resources.domain.value_objects import ResourceType, ResourceUrl


@dataclass
class UpdateResourceCommand:
    id_: UUID
    name: str
    url: str
    type: str


class UpdateResourceHandler:
    def __init__(self, resource_repository: ResourceRepositoryABC) -> None:
        self._resource_repository = resource_repository

    async def handle(self, command: UpdateResourceCommand) -> Resource:
        resource = await self._resource_repository.get_by_id(command.id_)
        resource.name = command.name
        resource.url = ResourceUrl(value=command.url)
        resource.type = ResourceType(value=command.type)
        return await self._resource_repository.save(resource)
