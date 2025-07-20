import uuid

import pytest
from odata_v4_query import ODataQueryOptions

from src.resources.application.list_resources import ListResourcesHandler
from src.resources.domain.entities import Resource
from src.resources.domain.value_objects import ResourceType, ResourceUrl
from src.resources.tests.application.mock_repository import MockResourcesRepository


@pytest.mark.asyncio
class TestListResource:
    async def test_list_resources(self):
        resource_repository = MockResourcesRepository()
        resource_repository.resources = {
            uuid.uuid4(): Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            ),
            uuid.uuid4(): Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.org'),
                type=ResourceType(value='image'),
            ),
        }

        resources = await ListResourcesHandler(resource_repository).handle()

        expected_resources_count = 2
        assert len(resources) == expected_resources_count
        assert resources[0].url == 'https://example.com'
        assert resources[1].url == 'https://example.org'

    async def test_limit_number_of_resources_returned(self):
        resource_repository = MockResourcesRepository()
        resource_repository.resources = {
            uuid.uuid4(): Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            ),
            uuid.uuid4(): Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.org'),
                type=ResourceType(value='image'),
            ),
        }

        resources = await ListResourcesHandler(resource_repository).handle(
            odata_options=ODataQueryOptions(top=1),
        )

        expected_resources_count = 1
        assert len(resources) == expected_resources_count
        assert resources[0].url == 'https://example.com'
