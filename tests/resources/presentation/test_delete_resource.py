import pytest
from fastapi import status
from fastapi.testclient import TestClient

from modules.resources.domain.entities import Resource
from shared.utils.uuid_tools import empty_uuid


class TestDeleteResource:
    def test_returns_204_after_deleting_resource(
        self,
        resource: Resource,
        client: TestClient,
    ):
        # Act
        response = client.delete(f'/resources/{resource.id}')

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.usefixtures('repo')
    def test_returns_204_when_deleting_resource_that_does_not_exist(
        self,
        client: TestClient,
    ):
        # Act
        response = client.delete(f'/resources/{empty_uuid()}')

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
