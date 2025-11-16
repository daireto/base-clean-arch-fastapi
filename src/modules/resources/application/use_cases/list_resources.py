from dataclasses import dataclass

from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.infrastructure.instrumentation.use_cases.list_resources import (
    ListResourcesInstrumentation,
)
from shared.application.interfaces.base import CommandHandler
from shared.domain.helpers.odata_helper import ODataHelper
from shared.domain.result import Result


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

    async def handle(self, command: ListResourcesCommand) -> Result[list[Resource]]:
        self._instrumentation.before()
        try:
            resources = await self._resource_repository.all(command.odata.get())
        except Exception as error:
            self._instrumentation.error(error)
            return Result.failure(error)
        self._instrumentation.after(resources)
        return Result.success(resources)

    async def handle_with_count(
        self, command: ListResourcesCommand
    ) -> Result[tuple[list[Resource], int]]:
        self._instrumentation.before()
        try:
            resources = await self._resource_repository.all(command.odata.get())
            total = await self._resource_repository.count(
                command.odata.get_for_counting()
            )
        except Exception as error:
            self._instrumentation.error(error)
            return Result.failure(error)
        self._instrumentation.after(resources)
        return Result.success((resources, total))
