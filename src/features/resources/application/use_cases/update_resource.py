from dataclasses import dataclass
from uuid import UUID

from features.resources.domain.entities import Resource
from features.resources.domain.errors import ResourceNotFoundError
from features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from features.resources.domain.value_objects import ResourceType, ResourceUrl
from features.resources.infrastructure.instrumentation.use_cases.update_resource import (
    UpdateResourceInstrumentation,
)
from shared.application.interfaces.base import CommandHandler
from shared.domain.result import Result


@dataclass
class UpdateResourceCommand:
    id: UUID
    name: str
    url: str
    type: str


class UpdateResourceHandler(CommandHandler):
    def __init__(
        self,
        resource_repository: ResourceRepositoryABC,
        instrumentation: UpdateResourceInstrumentation | None = None,
    ) -> None:
        self._resource_repository = resource_repository
        self._instrumentation = instrumentation or UpdateResourceInstrumentation()

    async def handle(self, command: UpdateResourceCommand) -> Result[Resource]:
        resource = Resource(
            id=command.id,
            name=command.name,
            url=ResourceUrl(value=command.url),
            type=ResourceType(value=command.type),
        )
        self._instrumentation.before(resource)
        try:
            updated = await self._resource_repository.update(resource)
        except Exception as error:
            self._instrumentation.error(error)
            return Result.failure(error)
        if not updated:
            self._instrumentation.not_found(resource)
            return Result.failure(ResourceNotFoundError(command.id))
        self._instrumentation.after(updated)
        return Result.success(updated)
