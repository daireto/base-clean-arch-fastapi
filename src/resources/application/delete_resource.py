from dataclasses import dataclass
from uuid import UUID

from src.resources.domain.repositories import ResourceRepositoryABC


@dataclass
class DeleteResourceCommand:
    id_: UUID | str


class DeleteResourceHandler:
    def __init__(self, resource_repository: ResourceRepositoryABC) -> None:
        self._resource_repository = resource_repository

    async def handle(self, command: DeleteResourceCommand) -> None:
        if isinstance(command.id_, str):
            command.id_ = UUID(command.id_)

        await self._resource_repository.delete(command.id_)
