import pytest
from odata_v4_query import ODataQueryOptions

from src.features.resources.application.use_cases.list_resources import (
    ListResourcesCommand,
    ListResourcesHandler,
)
from src.features.resources.domain.entities import Resource
from src.features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from src.shared.utils.odata_options import SafeODataQueryOptions


@pytest.mark.asyncio
class TestListResource:
    async def test_returns_all_available_resources_from_repository(
        self, repo: ResourceRepositoryABC, resources: list[Resource]
    ):
        # Act
        result = await ListResourcesHandler(repo).handle(
            ListResourcesCommand(
                odata_options=SafeODataQueryOptions(ODataQueryOptions(top=10)),
            ),
        )
        listed_resources = result.get_value_or_raise()

        # Assert
        assert len(listed_resources) == len(resources)
        assert listed_resources[0].url == 'https://example.com'
        assert listed_resources[1].url == 'https://example.org'

    @pytest.mark.usefixtures('resources')
    async def test_returns_only_requested_number_of_resources(
        self, repo: ResourceRepositoryABC
    ):
        # Arrange
        limit = 1

        # Act
        result = await ListResourcesHandler(repo).handle(
            ListResourcesCommand(
                odata_options=SafeODataQueryOptions(ODataQueryOptions(top=limit)),
            ),
        )
        listed_resources = result.get_value_or_raise()

        # Assert
        assert len(listed_resources) == limit
        assert listed_resources[0].url == 'https://example.com'
