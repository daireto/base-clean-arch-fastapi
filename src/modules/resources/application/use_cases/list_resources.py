from dataclasses import dataclass

from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.infrastructure.instrumentation.use_cases.list_resources import (
    ListResourcesInstrumentation,
)
from shared.application.interfaces.base import CommandHandler
from shared.utils.odata_options import SafeODataQueryOptions
from shared.utils.result import Result


@dataclass
class ListResourcesCommand:
    odata_options: SafeODataQueryOptions


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
            resources = await self._resource_repository.all(
                command.odata_options.get_sanitized()
            )
        except Exception as error:
            self._instrumentation.error(error)
            return Result.failure(error)
        self._instrumentation.after(resources)
        return Result.success(resources)
