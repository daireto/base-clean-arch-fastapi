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
class TestUpdateResource:
    async def test_returns_200_and_resource_details(self, resource: Resource):
        # Arrange
        data = {
            'name': 'Random Image',
            'url': 'https://picsum.photos/200/200',
            'type': 'image',
        }

        # Act
        with TestClient(app) as client:
            response = client.put(f'/resources/{resource.id}', json=data)
        response_content = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response_content['resource']['id'] == str(resource.id)
        assert response_content['resource']['name'] == data['name']
        assert response_content['resource']['url'] == data['url']
        assert response_content['resource']['type'] == data['type']

    async def test_returns_400_when_resource_url_is_invalid(self, resource: Resource):
        # Arrange
        data = {
            'name': 'Random Image',
            'url': 'not-a-valid-url',
            'type': 'image',
        }

        # Act
        with TestClient(app) as client:
            response = client.put(f'/resources/{resource.id}', json=data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_returns_400_when_resource_type_is_not_supported(
        self, resource: Resource
    ):
        # Arrange
        data = {
            'name': 'Random Image',
            'url': 'https://example.com',
            'type': 'not-a-valid-type',
        }

        # Act
        with TestClient(app) as client:
            response = client.put(f'/resources/{resource.id}', json=data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_returns_404_when_resource_does_not_exist(
        self,
    ):
        # Arrange
        data = {
            'name': 'Random Image',
            'url': 'https://example.com',
            'type': 'image',
        }

        # Act
        with TestClient(app) as client:
            response = client.put(f'/resources/{empty_uuid()}', json=data)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
