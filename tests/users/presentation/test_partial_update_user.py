from fastapi import status
from fastapi.testclient import TestClient

from modules.users.domain.entities import User
from shared.utils.uuid_tools import uuid


class TestUpdateUser:
    def test_returns_200_when_user_exists(self, user: User, client: TestClient):
        data = {
            'fullname': 'Test User Updated',
        }

        response = client.patch(f'/users/{user.id}', json=data)
        content = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert content['user']['id'] == str(user.id)
        assert content['user']['fullname'] == data['fullname']
        assert content['user']['username'] == user.username

    def test_returns_404_when_user_does_not_exist(
        self,
        client: TestClient,
    ):
        data = {
            'fullname': 'Test User Updated',
        }

        response = client.patch(f'/users/{uuid()}', json=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_422_when_user_email_is_invalid(
        self,
        user: User,
        client: TestClient,
    ):
        data = {
            'email': 'not-a-valid-email',
        }

        response = client.patch(f'/users/{user.id}', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_user_gender_is_not_supported(
        self,
        user: User,
        client: TestClient,
    ):
        data = {
            'gender': 'not-a-valid-gender',
        }

        response = client.patch(f'/users/{user.id}', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_user_role_is_not_supported(
        self,
        user: User,
        client: TestClient,
    ):
        data = {
            'role': 'not-a-valid-role',
        }

        response = client.patch(f'/users/{user.id}', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
