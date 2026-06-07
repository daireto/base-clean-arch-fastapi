import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.usefixtures('users_repo')
class TestCreateUser:
    def test_returns_201_when_user_is_created(
        self,
        client: TestClient,
    ):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User 1',
            'email': 'testuser1@example.com',
            'gender': 'male',
            'password': 'password123',
        }

        response = client.post('/users/', json=data)
        response_content = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert response_content['user']['username'] == data['username']

    def test_returns_422_when_user_email_is_invalid(self, client: TestClient):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User 1',
            'email': 'not-a-valid-email',
            'gender': 'male',
            'password': 'password123',
        }

        response = client.post('/users/', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_user_gender_is_not_supported(self, client: TestClient):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User 1',
            'email': 'testuser1@example.com',
            'gender': 'not-a-valid-gender',
            'password': 'password123',
        }

        response = client.post('/users/', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_user_password_is_too_short(self, client: TestClient):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User 1',
            'email': 'testuser1@example.com',
            'gender': 'male',
            'password': 'short',
        }

        response = client.post('/users/', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_returns_422_when_user_password_is_too_long(self, client: TestClient):
        data = {
            'username': 'testuser1',
            'fullname': 'Test User 1',
            'email': 'testuser1@example.com',
            'gender': 'male',
            'password': 'a' * 129,
        }

        response = client.post('/users/', json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
