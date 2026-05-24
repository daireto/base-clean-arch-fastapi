from uuid import UUID

from pydantic import BaseModel
from simple_result import Err, Ok, Result

from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from modules.resources.infrastructure.instrumentation.use_cases.delete_resource import (
    DeleteResourceInstrumentation,
)
from shared.application.command_handler import CommandHandler
from shared.application.instrumentation import NoInstrumentation


class DeleteResourceCommand(BaseModel):
    id: UUID


class DeleteResourceHandler(CommandHandler):
    def __init__(
        self,
        resource_repository: ResourceRepositoryABC,
        instrumentation: DeleteResourceInstrumentation | None = None,
    ) -> None:
        self._resource_repository = resource_repository
        self._instrumentation = instrumentation or NoInstrumentation()

    async def handle(self, command: DeleteResourceCommand) -> Result[None, Exception]:
        self._instrumentation.before(command.id)

        try:
            await self._resource_repository.delete(command.id)
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(command.id)
        return Ok(None)
