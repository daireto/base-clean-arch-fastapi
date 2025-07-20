import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app
from src.resources.di import container
from src.resources.domain.entities import Resource
from src.resources.domain.repositories import ResourceRepositoryABC
from src.resources.domain.value_objects import ResourceType, ResourceUrl


@pytest.mark.asyncio
class TestUpdateResource:
    async def test_update_resource_and_return_200(self):
        repo = container[ResourceRepositoryABC]
        resource = await repo.create(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            )
        )
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
