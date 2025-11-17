from dataclasses import dataclass
from uuid import UUID

from simple_result import Err, Ok, Result

from modules.resources.domain.entities import Resource
from modules.resources.domain.exceptions import ResourceNotFoundError
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.domain.value_objects import ResourceType, ResourceUrl
from modules.resources.infrastructure.instrumentation.use_cases.update_resource import (
    UpdateResourceInstrumentation,
)
from shared.application.interfaces.base import CommandHandler


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

    async def handle(
        self,
        command: UpdateResourceCommand,
    ) -> Result[Resource, Exception]:
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
            return Err(error)
        if not updated:
            self._instrumentation.not_found(resource)
            return Err(ResourceNotFoundError(command.id))
        self._instrumentation.after(updated)
        return Ok(updated)
