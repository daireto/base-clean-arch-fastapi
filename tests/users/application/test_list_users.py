import pytest
from odata_v4_query import ODataQueryOptions

from modules.users.application.use_cases.list_users import (
    ListUsersCommand,
    ListUsersHandler,
)
from modules.users.domain.entities import User
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from shared.helpers.odata_helper import ODataHelper


@pytest.mark.asyncio
class TestListUser:
    async def test_returns_all_available_users(
        self, users_repo: UserRepositoryABC, users: list[User]
    ):
        result = await ListUsersHandler(users_repo).handle(
            ListUsersCommand(
                odata=ODataHelper(ODataQueryOptions(top=10), max_top=100),
            ),
        )

        assert result
        listed_users = result.unwrap_value()
        assert len(listed_users) == len(users)
        assert listed_users[0].username == users[0].username
        assert listed_users[1].username == users[1].username

    @pytest.mark.usefixtures('users')
    async def test_returns_only_requested_number_of_users(
        self, users_repo: UserRepositoryABC, users: list[User]
    ):
        limit = 1

        result = await ListUsersHandler(users_repo).handle(
            ListUsersCommand(
                odata=ODataHelper(ODataQueryOptions(top=limit), max_top=100),
            ),
        )

        assert result
        listed_users = result.unwrap_value()
        assert len(listed_users) == limit
        assert listed_users[0].username == users[0].username
