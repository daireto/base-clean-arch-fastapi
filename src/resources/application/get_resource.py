from dataclasses import dataclass
from uuid import UUID

from src.resources.domain.entities import Resource
from src.resources.domain.repositories import ResourceRepositoryABC


@dataclass
class GetResourceCommand:
    id_: UUID


class GetResourceHandler:
    def __init__(self, resource_repository: ResourceRepositoryABC) -> None:
        self._resource_repository = resource_repository

    async def handle(self, command: GetResourceCommand) -> Resource:
        return await self._resource_repository.get_by_id(command.id_)
