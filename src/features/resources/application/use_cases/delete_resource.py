from dataclasses import dataclass
from uuid import UUID

from features.resources.domain.errors import ResourceNotFoundError
from features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from features.resources.infrastructure.instrumentation.use_cases.delete_resource import (
    DeleteResourceInstrumentation,
)
from shared.application.interfaces.base import CommandHandler
from shared.domain.result import Result


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

    async def handle(self, command: DeleteResourceCommand) -> Result[None]:
        self._instrumentation.before(command.id)
        try:
            deleted = await self._resource_repository.delete(command.id)
        except Exception as error:
            self._instrumentation.error(error)
            return Result.failure(error)
        if not deleted:
            self._instrumentation.not_found(command.id)
            return Result.failure(ResourceNotFoundError(command.id))
        self._instrumentation.after(command.id)
        return Result.success()
