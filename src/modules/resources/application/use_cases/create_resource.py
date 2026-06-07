from pydantic import BaseModel, HttpUrl
from simple_result import Err, Ok, Result

from modules.resources.domain.entities import Resource
from modules.resources.domain.enums import MediaType
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from modules.resources.domain.value_objects import ResourceUrl
from shared.application.instrumentation import CreationUseCaseInstrumentation
from shared.application.interfaces.command_handler import CommandHandler


class CreateResourceCommand(BaseModel):
    name: str
    url: HttpUrl | str
    type: MediaType | str


class CreateResourceHandler(CommandHandler):
    def __init__(
        self,
        resource_repository: ResourceRepositoryABC,
        instrumentation: CreationUseCaseInstrumentation[Resource] | None = None,
    ) -> None:
        self._resource_repository = resource_repository
        self._instrumentation = instrumentation or CreationUseCaseInstrumentation()

    async def handle(
        self,
        command: CreateResourceCommand,
    ) -> Result[Resource, Exception]:
        resource = Resource(
            name=command.name,
            url=ResourceUrl(value=command.url),  # type: ignore
            type=command.type,  # type: ignore
        )
        self._instrumentation.before(resource)

        try:
            created = await self._resource_repository.create(resource)
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(created)
        return Ok(created)
