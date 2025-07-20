from dataclasses import dataclass
from uuid import UUID

from src.resources.domain.entities import Resource
from src.resources.domain.repositories import ResourceRepositoryABC
from src.resources.domain.value_objects import ResourceType, ResourceUrl


@dataclass
class UpdateResourceCommand:
    id_: UUID | str
    name: str
    url: str
    type: str


class UpdateResourceHandler:
    def __init__(self, resource_repository: ResourceRepositoryABC) -> None:
        self._resource_repository = resource_repository

    async def handle(self, command: UpdateResourceCommand) -> Resource:
        if isinstance(command.id_, str):
            command.id_ = UUID(command.id_)

        resource = Resource(
            id=command.id_,
            name=command.name,
            url=ResourceUrl(value=command.url),
            type=ResourceType(value=command.type),
        )
        return await self._resource_repository.update(resource)
