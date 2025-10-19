import pytest
import pytest_asyncio
from fastapi import status
from fastapi.testclient import TestClient
from odata_v4_query import ODataQueryOptions

from main import app
from src.core.config import settings
from src.features.resources.domain.entities import Resource
from src.features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from src.features.resources.domain.value_objects import ResourceType, ResourceUrl


@pytest_asyncio.fixture()
async def resources(repo: ResourceRepositoryABC):
    current_resources = await repo.all(
        odata_options=ODataQueryOptions(top=settings.max_records_per_page),
    )
    for resource in current_resources:
        await repo.delete(resource.id)

    return [
        await repo.create(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            )
        ),
        await repo.create(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.org'),
                type=ResourceType(value='image'),
            )
        ),
    ]


@pytest.mark.asyncio(loop_scope='module')
class TestListResources:
    async def test_returns_200_and_all_resources(self, resources: list[Resource]):
        # Act
        with TestClient(app) as client:
            response = client.get('/resources/')
        response_content = response.json()
        retrieved_resources = response_content['resources']

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(retrieved_resources) == len(resources)

    @pytest.mark.usefixtures('resources')
    async def test_returns_200_and_limit_number_of_resources_returned(self):
        # Act
        with TestClient(app) as client:
            response = client.get('/resources/?$top=1')
        response_content = response.json()
        retrieved_resources = response_content['resources']

        # Assert
        assert response.status_code == status.HTTP_200_OK
        expected_resources_count = 1
        assert len(retrieved_resources) == expected_resources_count
