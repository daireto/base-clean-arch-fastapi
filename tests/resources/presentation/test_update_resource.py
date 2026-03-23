import pytest
from fastapi import status
from fastapi.testclient import TestClient

from modules.resources.domain.entities import Resource
from shared.utils.uuid_tools import empty_uuid


class TestUpdateResource:
    def test_returns_200_with_resource_details_after_updating_resource(
        self,
        resource: Resource,
        client: TestClient,
    ):
        # Arrange
        data = {
            'name': 'Random Image',
            'url': 'https://picsum.photos/200/200',
            'type': 'image',
        }

        # Act
        response = client.put(f'/resources/{resource.id}', json=data)
        response_content = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response_content['resource']['id'] == str(resource.id)
        assert response_content['resource']['name'] == data['name']
        assert response_content['resource']['url'] == data['url']
        assert response_content['resource']['type'] == data['type']

    @pytest.mark.usefixtures('repo')
    def test_returns_200_with_resource_details_after_creating_resource_when_it_does_not_exist(
        self,
        client: TestClient,
    ):
        # Arrange
        data = {
            'name': 'Random Image',
            'url': 'https://example.com/',
            'type': 'image',
        }

        # Act
        response = client.put(f'/resources/{empty_uuid()}', json=data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['resource']['name'] == data['name']
        assert response.json()['resource']['url'] == data['url']
        assert response.json()['resource']['type'] == data['type']

    def test_returns_422_when_resource_url_is_invalid(
        self,
        resource: Resource,
        client: TestClient,
    ):
        # Arrange
        data = {
            'name': 'Random Image',
            'url': 'not-a-valid-url',
            'type': 'image',
        }

        # Act
        response = client.put(f'/resources/{resource.id}', json=data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_returns_422_when_resource_type_is_not_supported(
        self,
        resource: Resource,
        client: TestClient,
    ):
        # Arrange
        data = {
            'name': 'Random Image',
            'url': 'https://example.com/',
            'type': 'not-a-valid-type',
        }

        # Act
        response = client.put(f'/resources/{resource.id}', json=data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
