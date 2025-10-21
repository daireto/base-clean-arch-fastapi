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
class TestDeleteResource:
    async def test_returns_204(self, resource: Resource):
        # Act
        with TestClient(app) as client:
            response = client.delete(f'/resources/{resource.id}')

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_returns_404_when_resource_does_not_exist(
        self,
    ):
        # Act
        with TestClient(app) as client:
            response = client.get(f'/resources/{empty_uuid()}')

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
