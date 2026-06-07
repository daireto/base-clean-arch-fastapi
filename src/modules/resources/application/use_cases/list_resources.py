from pydantic import BaseModel, ConfigDict
from simple_result import Err, Ok, Result

from modules.resources.domain.collections import ResourceCollection
from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from shared.application.instrumentation import ListingUseCaseInstrumentation
from shared.application.interfaces.command_handler import CommandHandler
from shared.helpers.odata_helper import ODataHelper


class ListResourcesCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    odata: ODataHelper


class ListResourcesHandler(CommandHandler):
    def __init__(
        self,
        resource_repository: ResourceRepositoryABC,
        instrumentation: ListingUseCaseInstrumentation[Resource] | None = None,
    ) -> None:
        self._resource_repository = resource_repository
        self._instrumentation = instrumentation or ListingUseCaseInstrumentation()

    async def handle(
        self,
        command: ListResourcesCommand,
    ) -> Result[ResourceCollection, Exception]:
        self._instrumentation.before()

        try:
            resources = await self._resource_repository.all(command.odata.get())
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(resources)
        return Ok(ResourceCollection(resources))

    async def handle_with_count(
        self,
        command: ListResourcesCommand,
    ) -> Result[ResourceCollection, Exception]:
        self._instrumentation.before()

        try:
            resources = await self._resource_repository.all(command.odata.get())
            total = await self._resource_repository.count(
                command.odata.get_for_counting()
            )
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(resources)
        return Ok(ResourceCollection(resources, total))
