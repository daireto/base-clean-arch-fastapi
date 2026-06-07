import pytest
from fastapi import status
from fastapi.testclient import TestClient

from modules.users.domain.entities import User
from shared.utils.uuid_tools import uuid


class TestDeleteUser:
    def test_returns_204_when_user_is_deleted(
        self,
        user: User,
        client: TestClient,
    ):
        response = client.delete(f'/users/{user.id}')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.usefixtures('users_repo')
    def test_returns_204_when_user_does_not_exist(
        self,
        client: TestClient,
    ):
        response = client.delete(f'/users/{uuid()}')

        assert response.status_code == status.HTTP_204_NO_CONTENT
