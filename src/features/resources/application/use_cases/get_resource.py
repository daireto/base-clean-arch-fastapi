from dataclasses import dataclass
from uuid import UUID

from features.resources.domain.entities import Resource
from features.resources.domain.errors import ResourceNotFoundError
from features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from features.resources.infrastructure.instrumentation.use_cases.get_resource import (
    GetResourceInstrumentation,
)
from shared.application.interfaces.base import CommandHandler
from shared.domain.result import Result


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
