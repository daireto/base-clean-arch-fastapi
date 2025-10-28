import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from modules.resources.domain.entities import Resource
from shared.utils.uuid_tools import empty_uuid


class TestGetResource:
    def test_returns_200_and_resource_details(self, resource: Resource):
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

    @pytest.mark.usefixtures('repo')
    def test_returns_404_when_resource_does_not_exist(self):
        # Act
        with TestClient(app) as client:
            response = client.get(f'/resources/{empty_uuid()}')

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
