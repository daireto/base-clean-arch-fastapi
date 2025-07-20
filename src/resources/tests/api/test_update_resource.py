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
class TestUpdateResource:
    async def test_update_resource_and_return_200(self, resource: Resource):
        data = {
            'name': 'Random Image',
            'url': 'https://picsum.photos/200/200',
            'type': 'image',
        }

        with TestClient(app) as client:
            response = client.put(f'/resources/{resource.id}', json=data)

        assert response.status_code == status.HTTP_200_OK

        response_content = response.json()
        assert response_content['id'] == str(resource.id)
        assert response_content['name'] == data['name']
        assert response_content['url'] == data['url']
        assert response_content['type'] == data['type']

    async def test_raise_when_resource_url_is_invalid_and_return_400(
        self, resource: Resource
    ):
        data = {
            'name': 'Random Image',
            'url': 'not-a-valid-url',
            'type': 'image',
        }

        with TestClient(app) as client:
            response = client.put(f'/resources/{resource.id}', json=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_raise_when_resource_type_is_not_supported_and_return_400(
        self, resource: Resource
    ):
        data = {
            'name': 'Random Image',
            'url': 'https://example.com',
            'type': 'not-a-valid-type',
        }

        with TestClient(app) as client:
            response = client.put(f'/resources/{resource.id}', json=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_raise_when_updating_resource_that_does_not_exist_and_return_404(
        self,
    ):
        data = {
            'name': 'Random Image',
            'url': 'https://example.com',
            'type': 'image',
        }

        with TestClient(app) as client:
            response = client.put(f'/resources/{empty_uuid()}', json=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
