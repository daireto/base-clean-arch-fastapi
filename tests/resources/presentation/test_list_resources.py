import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from modules.resources.domain.entities import Resource


class TestListResources:
    def test_returns_200_with_all_resources_when_no_query_params_are_provided(
        self, resources: list[Resource]
    ):
        # Act
        with TestClient(app) as client:
            response = client.get('/resources/')
        response_content = response.json()
        retrieved_resources = response_content['items']

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(retrieved_resources) == len(resources)
        assert response_content['total'] == len(resources)
        assert response_content['skip'] == 0
        assert response_content['page'] == 1

    @pytest.mark.usefixtures('resources')
    def test_returns_200_with_limited_resources_returned_when_top_param_is_provided(
        self,
    ):
        # Arrange
        limit = 1

        # Act
        with TestClient(app) as client:
            response = client.get(f'/resources/?$top={limit}')
        response_content = response.json()
        retrieved_resources = response_content['items']

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(retrieved_resources) == limit

    @pytest.mark.usefixtures('resources')
    def test_returns_200_with_skipped_resources_when_skip_param_is_provided(self):
        # Arrange
        skip = 1
        expected_resources = 1

        # Act
        with TestClient(app) as client:
            response = client.get(f'/resources/?$skip={skip}')
        response_content = response.json()
        retrieved_resources = response_content['items']

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(retrieved_resources) == expected_resources

    @pytest.mark.usefixtures('resources')
    def test_returns_200_with_skipped_limited_resources_when_page_param_is_provided(
        self,
    ):
        # Arrange
        page = 2
        page_size = 1

        # Act
        with TestClient(app) as client:
            response = client.get(f'/resources/?$page={page}&$top={page_size}')
        response_content = response.json()
        retrieved_resources = response_content['items']

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(retrieved_resources) == page_size
        assert response_content['skip'] == page_size
