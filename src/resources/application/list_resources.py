from odata_v4_query import ODataQueryOptions

from src.resources.domain.entities import Resource
from src.resources.domain.repositories import ResourceRepositoryABC
from src.shared import settings


class ListResourcesHandler:
    def __init__(self, resource_repository: ResourceRepositoryABC) -> None:
        self._resource_repository = resource_repository

    async def handle(
        self,
        odata_options: ODataQueryOptions | None = None,
    ) -> list[Resource]:
        if not odata_options:
            odata_options = ODataQueryOptions(top=settings.MAX_RECORDS_PER_PAGE)

        if odata_options.top and odata_options.top > settings.MAX_RECORDS_PER_PAGE:
            odata_options.top = settings.MAX_RECORDS_PER_PAGE

        return await self._resource_repository.all(odata_options)
