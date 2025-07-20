from dataclasses import dataclass

from src.resources.domain.entities import Resource
from src.resources.domain.repositories import ResourceRepositoryABC
from src.resources.domain.value_objects import ResourceType, ResourceUrl


@dataclass
class CreateResourceCommand:
    name: str
    url: str
    type: str


class CreateResourceHandler:
    def __init__(self, resource_repository: ResourceRepositoryABC) -> None:
        self._resource_repository = resource_repository

    async def handle(self, command: CreateResourceCommand) -> Resource:
        resource = Resource(
            name=command.name,
            url=ResourceUrl(value=command.url),
            type=ResourceType(value=command.type),
        )
        return await self._resource_repository.create(resource)
