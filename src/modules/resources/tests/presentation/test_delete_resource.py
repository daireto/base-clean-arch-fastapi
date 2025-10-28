import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from modules.resources.domain.entities import Resource
from shared.utils.uuid_tools import empty_uuid


class TestDeleteResource:
    def test_returns_204_after_deleting_resource(self, resource: Resource):
        # Act
        with TestClient(app) as client:
            response = client.delete(f'/resources/{resource.id}')

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.usefixtures('repo')
    def test_returns_404_when_resource_does_not_exist(self):
        # Act
        with TestClient(app) as client:
            response = client.get(f'/resources/{empty_uuid()}')

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
