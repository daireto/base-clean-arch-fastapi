import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from src.features.resources.domain.entities import Resource


class TestListResources:
    def test_returns_200_and_all_resources_details(self, resources: list[Resource]):
        # Act
        with TestClient(app) as client:
            response = client.get('/resources/')
        response_content = response.json()
        retrieved_resources = response_content['resources']

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(retrieved_resources) == len(resources)

    @pytest.mark.usefixtures('resources')
    def test_returns_200_and_limit_number_of_resources_returned(self):
        # Arrange
        limit = 1

        # Act
        with TestClient(app) as client:
            response = client.get(f'/resources/?$top={limit}')
        response_content = response.json()
        retrieved_resources = response_content['resources']

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(retrieved_resources) == limit
