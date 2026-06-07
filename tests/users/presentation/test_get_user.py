import pytest
from fastapi import status
from fastapi.testclient import TestClient

from modules.users.domain.entities import User
from shared.utils.uuid_tools import uuid


class TestGetUser:
    def test_returns_200_when_user_exists(
        self,
        user: User,
        client: TestClient,
    ):
        response = client.get(f'/users/{user.id}')
        response_content = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_content['user']['id'] == str(user.id)
        assert response_content['user']['username'] == user.username
        assert response_content['user']['fullname'] == user.fullname

    @pytest.mark.usefixtures('users_repo')
    def test_returns_404_when_user_does_not_exist(self, client: TestClient):
        response = client.get(f'/users/{uuid()}')

        assert response.status_code == status.HTTP_404_NOT_FOUND
