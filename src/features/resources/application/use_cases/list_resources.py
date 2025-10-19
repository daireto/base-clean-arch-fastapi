from odata_v4_query import ODataQueryOptions

from src.core.config import settings
from src.features.resources.application.instrumentation.list_resources import (
    ListResourcesInstrumentation,
)
from src.features.resources.domain.entities import Resource
from src.features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from src.shared.application.interfaces.base import CommandHandler
from src.shared.domain.result import Result


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
        odata_options: ODataQueryOptions | None = None,
    ) -> Result[list[Resource]]:
        if not odata_options:
            odata_options = ODataQueryOptions(top=settings.max_records_per_page)

        self._instrumentation.before()
        try:
            resources = await self._resource_repository.all(odata_options)
        except Exception as error:
            self._instrumentation.error(error)
            return Result.failure(error)
        self._instrumentation.after(resources)
        return Result.success(resources)
