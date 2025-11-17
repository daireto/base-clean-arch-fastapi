from dataclasses import dataclass
from uuid import UUID

from simple_result import Err, Ok, Result

from modules.resources.domain.exceptions import ResourceNotFoundError
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.infrastructure.instrumentation.use_cases.delete_resource import (
    DeleteResourceInstrumentation,
)
from shared.application.interfaces.base import CommandHandler


@dataclass
class DeleteResourceCommand:
    id: UUID


class DeleteResourceHandler(CommandHandler):
    def __init__(
        self,
        resource_repository: ResourceRepositoryABC,
        instrumentation: DeleteResourceInstrumentation | None = None,
    ) -> None:
        self._resource_repository = resource_repository
        self._instrumentation = instrumentation or DeleteResourceInstrumentation()

    async def handle(self, command: DeleteResourceCommand) -> Result[None, Exception]:
        self._instrumentation.before(command.id)
        try:
            deleted = await self._resource_repository.delete(command.id)
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)
        if not deleted:
            self._instrumentation.not_found(command.id)
            return Err(ResourceNotFoundError(command.id))
        self._instrumentation.after(command.id)
        return Ok(None)
