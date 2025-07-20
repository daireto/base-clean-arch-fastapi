import pytest
import pytest_asyncio
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app
from src.resources.di import container
from src.resources.domain.entities import Resource
from src.resources.domain.repositories import ResourceRepositoryABC
from src.resources.domain.value_objects import ResourceType, ResourceUrl
from src.shared.domain.utils import empty_uuid


@pytest_asyncio.fixture()
async def resource():
    repo = container[ResourceRepositoryABC]
    return await repo.create(
        Resource(
            name='Random Image',
            url=ResourceUrl(value='https://example.com'),
            type=ResourceType(value='image'),
        )
    )


@pytest.mark.asyncio
class TestGetResource:
    async def test_get_resource_and_return_200(self, resource: Resource):
        with TestClient(app) as client:
            response = client.get(f'/resources/{resource.id}')

        assert response.status_code == status.HTTP_200_OK

        response_content = response.json()
        assert response_content['id'] == str(resource.id)
        assert response_content['name'] == 'Random Image'
        assert response_content['url'] == 'https://example.com'
        assert response_content['type'] == 'image'

    async def test_raise_when_updating_resource_that_does_not_exist_and_return_404(
        self,
    ):
        with TestClient(app) as client:
            response = client.get(f'/resources/{empty_uuid()}')

        assert response.status_code == status.HTTP_404_NOT_FOUND
