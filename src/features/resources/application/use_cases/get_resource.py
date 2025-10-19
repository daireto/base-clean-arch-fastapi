from dataclasses import dataclass
from uuid import UUID

from src.features.resources.application.instrumentation.get_resource import (
    GetResourceInstrumentation,
)
from src.features.resources.domain.entities import Resource
from src.features.resources.domain.errors import ResourceNotFoundError
from src.features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from src.shared.application.interfaces.base import CommandHandler
from src.shared.domain.result import Result


@dataclass
class GetResourceCommand:
    id: UUID


class GetResourceHandler(CommandHandler):
    def __init__(
        self,
        resource_repository: ResourceRepositoryABC,
        instrumentation: GetResourceInstrumentation | None = None,
    ) -> None:
        self._resource_repository = resource_repository
        self._instrumentation = instrumentation or GetResourceInstrumentation()

    async def handle(self, command: GetResourceCommand) -> Result[Resource]:
        self._instrumentation.before(command.id)
        try:
            resource = await self._resource_repository.get_by_id(command.id)
        except Exception as error:
            self._instrumentation.error(error)
            return Result.failure(error)
        if not resource:
            self._instrumentation.not_found(command.id)
            return Result.failure(ResourceNotFoundError(command.id))
        self._instrumentation.after(resource)
        return Result.success(resource)
