from dataclasses import dataclass

from odata_v4_query import ODataQueryOptions

from src.features.resources.domain.entities import Resource
from src.features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from src.features.resources.infrastructure.instrumentation.use_cases.list_resources import (
    ListResourcesInstrumentation,
)
from src.shared.application.interfaces.base import CommandHandler
from src.shared.domain.result import Result


@dataclass
class ListResourcesCommand:
    odata_options: ODataQueryOptions


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
            resources = await self._resource_repository.all(command.odata_options)
        except Exception as error:
            self._instrumentation.error(error)
            return Result.failure(error)
        self._instrumentation.after(resources)
        return Result.success(resources)
