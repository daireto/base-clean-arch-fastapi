from uuid import UUID

from pydantic import BaseModel
from simple_result import Err, Ok, Result

from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from shared.application.instrumentation import DeletionUseCaseInstrumentation
from shared.application.interfaces.command_handler import CommandHandler


class DeleteResourceCommand(BaseModel):
    id: UUID


class DeleteResourceHandler(CommandHandler):
    def __init__(
        self,
        resource_repository: ResourceRepositoryABC,
        instrumentation: DeletionUseCaseInstrumentation | None = None,
    ) -> None:
        self._resource_repository = resource_repository
        self._instrumentation = instrumentation or DeletionUseCaseInstrumentation()

    async def handle(self, command: DeleteResourceCommand) -> Result[None, Exception]:
        self._instrumentation.before(command.id)

        try:
            await self._resource_repository.delete(command.id)
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(command.id)
        return Ok(None)
