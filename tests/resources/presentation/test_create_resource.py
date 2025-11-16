import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app


@pytest.mark.usefixtures('repo')
class TestCreateResource:
    def test_returns_200_with_resource_details_after_creating_resource(self):
        # Arrange
        data = {
            'name': 'Random Image',
            'url': 'https://picsum.photos/200/200',
            'type': 'image',
        }

        # Act
        with TestClient(app) as client:
            response = client.post('/resources/', json=data)
        response_content = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response_content['resource']['name'] == data['name']
        assert response_content['resource']['url'] == data['url']
        assert response_content['resource']['type'] == data['type']

    def test_returns_400_when_resource_url_is_invalid(self):
        # Arrange
        data = {
            'name': 'Random Image',
            'url': 'not-a-valid-url',
            'type': 'image',
        }

        # Act
        with TestClient(app) as client:
            response = client.post('/resources/', json=data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_400_when_resource_type_is_not_supported(self):
        # Arrange
        data = {
            'name': 'Random Image',
            'url': 'https://example.com',
            'type': 'not-a-valid-type',
        }

        # Act
        with TestClient(app) as client:
            response = client.post('/resources/', json=data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
