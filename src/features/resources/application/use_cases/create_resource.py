from dataclasses import dataclass

from src.features.resources.application.instrumentation.create_resource import (
    CreateResourceInstrumentation,
)
from src.features.resources.domain.entities import Resource
from src.features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from src.features.resources.domain.value_objects import ResourceType, ResourceUrl
from src.shared.application.interfaces.base import CommandHandler
from src.shared.domain.result import Result


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

    async def handle(self, command: CreateResourceCommand) -> Result[Resource]:
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
            return Result.failure(error)
        self._instrumentation.after(created)
        return Result.success(created)
