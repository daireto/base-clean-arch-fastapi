import pytest
from fastapi import status
from fastapi.testclient import TestClient

from modules.users.domain.entities import User
from shared.utils.uuid_tools import uuid


class TestUpdateUser:
    def test_returns_200_when_user_exists(
        self,
        user: User,
        client: TestClient,
    ):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User Updated',
            'email': 'testuser1@example.com',
            'gender': 'male',
        }

        response = client.put(f'/users/{user.id}', json=data)
        response_content = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_content['user']['id'] == str(user.id)
        assert response_content['user']['fullname'] == data['fullname']
        assert response_content['user']['username'] == data['username']
        assert response_content['user']['email'] == data['email']
        assert response_content['user']['gender'] == data['gender']

    @pytest.mark.usefixtures('users_repo')
    def test_returns_200_when_user_does_not_exist(
        self,
        client: TestClient,
    ):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User Updated',
            'email': 'testuser1@example.com',
            'gender': 'male',
            'password': 'password123',
        }

        response = client.put(f'/users/{uuid()}', json=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['user']['username'] == data['username']
        assert response.json()['user']['fullname'] == data['fullname']
        assert response.json()['user']['email'] == data['email']
        assert response.json()['user']['gender'] == data['gender']

    def test_returns_404_when_user_does_not_exist_and_password_is_not_provided(
        self,
        client: TestClient,
    ):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User Updated',
            'email': 'testuser1@example.com',
            'gender': 'male',
        }

        response = client.put(f'/users/{uuid()}', json=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_422_when_user_email_is_invalid(
        self,
        user: User,
        client: TestClient,
    ):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User Updated',
            'email': 'not-a-valid-email',
            'gender': 'male',
        }

        response = client.put(f'/users/{user.id}', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_user_gender_is_not_supported(
        self,
        user: User,
        client: TestClient,
    ):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User Updated',
            'email': 'testuser1@example.com',
            'gender': 'not-a-valid-gender',
        }

        response = client.put(f'/users/{user.id}', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_user_password_is_too_short(
        self,
        user: User,
        client: TestClient,
    ):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User Updated',
            'email': 'testuser1@example.com',
            'gender': 'male',
            'password': 'short',
        }

        response = client.put(f'/users/{user.id}', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_user_password_is_too_long(
        self,
        user: User,
        client: TestClient,
    ):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User Updated',
            'email': 'testuser1@example.com',
            'gender': 'male',
            'password': 'a' * 129,
        }

        response = client.put(f'/users/{user.id}', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
