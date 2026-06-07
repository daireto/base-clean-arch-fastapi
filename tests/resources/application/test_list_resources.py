import pytest
from odata_v4_query import ODataQueryOptions

from modules.resources.application.use_cases.list_resources import (
    ListResourcesCommand,
    ListResourcesHandler,
)
from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from shared.helpers.odata_helper import ODataHelper


@pytest.mark.asyncio
class TestListResource:
    async def test_returns_all_available_resources(
        self, resources_repo: ResourceRepositoryABC, resources: list[Resource]
    ):
        result = await ListResourcesHandler(resources_repo).handle(
            ListResourcesCommand(
                odata=ODataHelper(ODataQueryOptions(top=10), max_top=100),
            ),
        )

        assert result
        listed_resources = result.unwrap_value()
        assert len(listed_resources) == len(resources)
        assert str(listed_resources[0].url) == str(resources[0].url)
        assert str(listed_resources[1].url) == str(resources[1].url)

    @pytest.mark.usefixtures('resources')
    async def test_returns_only_requested_number_of_resources(
        self, resources_repo: ResourceRepositoryABC
    ):
        limit = 1

        result = await ListResourcesHandler(resources_repo).handle(
            ListResourcesCommand(
                odata=ODataHelper(ODataQueryOptions(top=limit), max_top=100),
            ),
        )

        assert result
        listed_resources = result.unwrap_value()
        assert len(listed_resources) == limit
        assert str(listed_resources[0].url) == 'https://example.com/'
