import pytest
import pytest_asyncio
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from src.features.resources.domain.entities import Resource
from src.features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from src.features.resources.domain.value_objects import ResourceType, ResourceUrl
from src.shared.utils.uuid_tools import empty_uuid


@pytest_asyncio.fixture()
async def resource(repo: ResourceRepositoryABC):
    return await repo.create(
        Resource(
            name='Random Image',
            url=ResourceUrl(value='https://example.com'),
            type=ResourceType(value='image'),
        )
    )


@pytest.mark.asyncio
class TestGetResource:
    async def test_returns_200_and_resource_details(self, resource: Resource):
        # Act
        with TestClient(app) as client:
            response = client.get(f'/resources/{resource.id}')
        response_content = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response_content['resource']['id'] == str(resource.id)
        assert response_content['resource']['name'] == 'Random Image'
        assert response_content['resource']['url'] == 'https://example.com'
        assert response_content['resource']['type'] == 'image'

    async def test_returns_404_when_resource_does_not_exist(self):
        # Act
        with TestClient(app) as client:
            response = client.get(f'/resources/{empty_uuid()}')

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
