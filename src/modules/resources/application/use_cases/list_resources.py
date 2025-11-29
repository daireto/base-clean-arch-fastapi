from dataclasses import dataclass

from simple_result import Err, Ok, Result

from modules.resources.domain.collections import ResourceCollection
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.infrastructure.instrumentation.use_cases.list_resources import (
    ListResourcesInstrumentation,
)
from shared.application.interfaces.base import CommandHandler
from shared.domain.helpers.odata_helper import ODataHelper


@dataclass
class ListResourcesCommand:
    odata: ODataHelper


class ListResourcesHandler(CommandHandler):
    def __init__(
        self,
        resource_repository: ResourceRepositoryABC,
        instrumentation: ListResourcesInstrumentation | None = None,
    ) -> None:
        self._resource_repository = resource_repository
        self._instrumentation = instrumentation or ListResourcesInstrumentation()

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
