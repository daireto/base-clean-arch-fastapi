from fastapi import status
from fastapi.testclient import TestClient

from modules.resources.domain.entities import Resource
from shared.utils.uuid_tools import uuid


class TestUpdateResource:
    def test_returns_200_when_resource_exists(
        self, resource: Resource, client: TestClient
    ):
        data = {
            'url': 'https://picsum.photos/200/200',
        }

        response = client.patch(f'/resources/{resource.id}', json=data)
        content = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert content['resource']['id'] == str(resource.id)
        assert content['resource']['name'] == resource.name
        assert content['resource']['url'] == data['url']
        assert content['resource']['type'] == resource.type

    def test_returns_404_when_resource_does_not_exist(
        self,
        client: TestClient,
    ):
        data = {
            'url': 'https://example.com/',
        }

        response = client.patch(f'/resources/{uuid()}', json=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_422_when_resource_url_is_invalid(
        self,
        resource: Resource,
        client: TestClient,
    ):
        data = {
            'url': 'not-a-valid-url',
        }

        response = client.patch(f'/resources/{resource.id}', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_resource_type_is_not_supported(
        self,
        resource: Resource,
        client: TestClient,
    ):
        data = {
            'type': 'not-a-valid-type',
        }

        response = client.patch(f'/resources/{resource.id}', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
