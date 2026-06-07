import pytest
from fastapi import status
from fastapi.testclient import TestClient

from modules.resources.domain.entities import Resource
from shared.utils.uuid_tools import uuid


class TestGetResource:
    def test_returns_200_when_resource_exists(
        self,
        resource: Resource,
        client: TestClient,
    ):
        response = client.get(f'/resources/{resource.id}')
        response_content = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_content['resource']['id'] == str(resource.id)
        assert response_content['resource']['name'] == resource.name
        assert response_content['resource']['url'] == str(resource.url)

    @pytest.mark.usefixtures('resources_repo')
    def test_returns_404_when_resource_does_not_exist(self, client: TestClient):
        response = client.get(f'/resources/{uuid()}')

        assert response.status_code == status.HTTP_404_NOT_FOUND
