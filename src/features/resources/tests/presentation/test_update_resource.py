import pytest
from fastapi import status
from fastapi.testclient import TestClient

from features.resources.domain.entities import Resource
from main import app
from shared.utils.uuid_tools import empty_uuid


class TestUpdateResource:
    def test_returns_200_and_resource_details(self, resource: Resource):
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

    def test_returns_400_when_resource_url_is_invalid(self, resource: Resource):
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

    def test_returns_400_when_resource_type_is_not_supported(self, resource: Resource):
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

    @pytest.mark.usefixtures('repo')
    def test_returns_404_when_resource_does_not_exist(
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
