import pytest
from fastapi import status
from fastapi.testclient import TestClient

from modules.users.domain.entities import User


class TestListUsers:
    def test_returns_200_with_all_users_when_no_query_params_are_provided(
        self,
        users: list[User],
        client: TestClient,
    ):
        response = client.get('/users/')
        response_content = response.json()
        retrieved_users = response_content['items']

        assert response.status_code == status.HTTP_200_OK
        assert len(retrieved_users) == len(users)
        assert response_content['total'] == len(users)
        assert response_content['skip'] == 0
        assert response_content['page'] == 1

    @pytest.mark.usefixtures('users')
    def test_returns_200_with_limited_users_returned_when_top_param_is_provided(
        self,
        client: TestClient,
    ):
        limit = 1

        response = client.get(f'/users/?$top={limit}')
        response_content = response.json()
        retrieved_users = response_content['items']

        assert response.status_code == status.HTTP_200_OK
        assert len(retrieved_users) == limit

    @pytest.mark.usefixtures('users')
    def test_returns_200_with_skipped_users_when_skip_param_is_provided(
        self,
        client: TestClient,
    ):
        skip = 1
        expected_users = 1

        response = client.get(f'/users/?$skip={skip}')
        response_content = response.json()
        retrieved_users = response_content['items']

        assert response.status_code == status.HTTP_200_OK
        assert len(retrieved_users) == expected_users

    @pytest.mark.usefixtures('users')
    def test_returns_200_with_skipped_limited_users_when_page_param_is_provided(
        self,
        client: TestClient,
    ):
        page = 2
        page_size = 1

        response = client.get(f'/users/?$page={page}&$top={page_size}')
        response_content = response.json()
        retrieved_users = response_content['items']

        assert response.status_code == status.HTTP_200_OK
        assert len(retrieved_users) == page_size
        assert response_content['skip'] == page_size
