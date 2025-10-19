import pytest
from odata_v4_query import ODataQueryOptions

from src.features.resources.application.use_cases.list_resources import (
    ListResourcesHandler,
)
from src.features.resources.domain.entities import Resource
from src.features.resources.domain.value_objects import ResourceType, ResourceUrl
from src.features.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)


@pytest.mark.asyncio
class TestListResource:
    async def test_returns_all_available_resources_from_repository(self):
        # Arrange
        repo = MockResourceRepository()
        expected_resources_count = 2
        await repo.create(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            )
        )
        await repo.create(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.org'),
                type=ResourceType(value='image'),
            )
        )

        # Act
        result = await ListResourcesHandler(repo).handle()
        resources = result.get_value_or_raise()

        # Assert
        assert len(resources) == expected_resources_count
        assert resources[0].url == 'https://example.com'
        assert resources[1].url == 'https://example.org'

    async def test_returns_only_requested_number_of_resources(self):
        # Arrange
        repo = MockResourceRepository()
        limit = 1
        await repo.create(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            )
        )
        await repo.create(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.org'),
                type=ResourceType(value='image'),
            )
        )

        # Act
        result = await ListResourcesHandler(repo).handle(
            odata_options=ODataQueryOptions(top=limit),
        )
        resources = result.get_value_or_raise()

        # Assert
        assert len(resources) == limit
        assert resources[0].url == 'https://example.com'
