import pytest
import pytest_asyncio
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app
from src.resources.di import container
from src.resources.domain.entities import Resource
from src.resources.domain.repositories import ResourceRepositoryABC
from src.resources.domain.value_objects import ResourceType, ResourceUrl


@pytest_asyncio.fixture()
async def resources():
    repo = container[ResourceRepositoryABC]
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


@pytest.mark.asyncio
class TestListResources:
    async def test_list_resources_and_return_200(self, resources: list[Resource]):
        with TestClient(app) as client:
            response = client.get('/resources/')

        assert response.status_code == status.HTTP_200_OK

        response_content = response.json()
        expected_resources_count = 2
        assert len(response_content) == expected_resources_count
        assert response_content[0]['id'] == str(resources[0].id)
        assert response_content[1]['id'] == str(resources[1].id)

    async def test_limit_number_of_resources_returned(self, resources: list[Resource]):
        with TestClient(app) as client:
            response = client.get('/resources/?$top=1')

        assert response.status_code == status.HTTP_200_OK

        response_content = response.json()
        expected_resources_count = 1
        assert len(response_content) == expected_resources_count
        assert response_content[0]['id'] == str(resources[0].id)
