from dataclasses import dataclass
from uuid import UUID

from src.resources.domain.repositories import ResourceRepositoryABC


@dataclass
class DeleteResourceCommand:
    id_: UUID


class DeleteResourceHandler:
    def __init__(self, resource_repository: ResourceRepositoryABC) -> None:
        self._resource_repository = resource_repository

    async def handle(self, command: DeleteResourceCommand) -> None:
        await self._resource_repository.delete(command.id_)
