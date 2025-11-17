from dataclasses import dataclass

from simple_result import Err, Ok, Result

from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.domain.value_objects import ResourceType, ResourceUrl
from modules.resources.infrastructure.instrumentation.use_cases.create_resource import (
    CreateResourceInstrumentation,
)
from shared.application.interfaces.base import CommandHandler


@dataclass
class CreateResourceCommand:
    name: str
    url: str
    type: str


class CreateResourceHandler(CommandHandler):
    def __init__(
        self,
        resource_repository: ResourceRepositoryABC,
        instrumentation: CreateResourceInstrumentation | None = None,
    ) -> None:
        self._resource_repository = resource_repository
        self._instrumentation = instrumentation or CreateResourceInstrumentation()

    async def handle(
        self,
        command: CreateResourceCommand,
    ) -> Result[Resource, Exception]:
        resource = Resource(
            name=command.name,
            url=ResourceUrl(value=command.url),
            type=ResourceType(value=command.type),
        )
        self._instrumentation.before(resource)
        try:
            created = await self._resource_repository.create(resource)
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)
        self._instrumentation.after(created)
        return Ok(created)
