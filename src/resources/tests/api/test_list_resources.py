import pytest
import pytest_asyncio
from fastapi import status
from fastapi.testclient import TestClient
from odata_v4_query import ODataQueryOptions

from src.main import app
from src.resources.di import container
from src.resources.domain.entities import Resource
from src.resources.domain.repositories import ResourceRepositoryABC
from src.resources.domain.value_objects import ResourceType, ResourceUrl
from src.shared import settings


@pytest_asyncio.fixture()
async def resources():
    repo = container[ResourceRepositoryABC]

    current_resources = await repo.all(
        odata_options=ODataQueryOptions(top=settings.MAX_RECORDS_PER_PAGE),
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
    async def test_list_resources_and_return_200(self, resources: list[Resource]):
        with TestClient(app) as client:
            response = client.get('/resources/')

        assert response.status_code == status.HTTP_200_OK

        response_content = response.json()
        assert len(response_content) == len(resources)

    async def test_limit_number_of_resources_returned(self):
        with TestClient(app) as client:
            response = client.get('/resources/?$top=1')

        assert response.status_code == status.HTTP_200_OK

        response_content = response.json()
        expected_resources_count = 1
        assert len(response_content) == expected_resources_count
