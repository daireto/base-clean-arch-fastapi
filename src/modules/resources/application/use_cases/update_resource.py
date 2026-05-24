from uuid import UUID

from pydantic import BaseModel, HttpUrl
from simple_result import Err, Ok, Result

from modules.resources.domain.entities import Resource
from modules.resources.domain.enums import MediaType
from modules.resources.domain.exceptions import ResourceNotFoundError
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from modules.resources.domain.value_objects import ResourceUrl
from modules.resources.infrastructure.instrumentation.use_cases.update_resource import (
    UpdateResourceInstrumentation,
)
from shared.application.command_handler import CommandHandler
from shared.application.instrumentation import NoInstrumentation


class UpdateResourceCommand(BaseModel):
    id: UUID
    name: str
    url: str | HttpUrl
    type: str | MediaType


class PartialUpdateResourceCommand(BaseModel):
    id: UUID
    name: str | None = None
    url: str | HttpUrl | None = None
    type: str | MediaType | None = None


class UpdateResourceHandler(CommandHandler):
    def __init__(
        self,
        resource_repository: ResourceRepositoryABC,
        instrumentation: UpdateResourceInstrumentation | None = None,
    ) -> None:
        self._resource_repository = resource_repository
        self._instrumentation = instrumentation or NoInstrumentation()

    async def handle(
        self,
        command: UpdateResourceCommand,
    ) -> Result[Resource, Exception]:
        resource = Resource(
            id=command.id,
            name=command.name,
            url=ResourceUrl(command.url),  # type: ignore
            type=command.type,  # type: ignore
        )
        self._instrumentation.before(resource)

        try:
            updated = await self._resource_repository.update(resource)
            if not updated:
                updated = await self._resource_repository.create(resource)
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(updated, created=not bool(resource))
        return Ok(updated)

    async def handle_partial(
        self,
        command: PartialUpdateResourceCommand,
    ) -> Result[Resource, Exception]:
        resource = await self._resource_repository.get_by_id(command.id)
        if not resource:
            self._instrumentation.not_found(command.id)
            return Err(ResourceNotFoundError(command.id))

        self._instrumentation.before(resource)
        resource = resource.update(command)

        try:
            updated = await self._resource_repository.update(resource)
            if not updated:
                self._instrumentation.not_found(resource.id)
                return Err(ResourceNotFoundError(resource.id))
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(updated)
        return Ok(updated)
