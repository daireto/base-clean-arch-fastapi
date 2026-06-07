import pytest

from modules.users.application.use_cases.get_user import (
    GetUserCommand,
    GetUserHandler,
)
from modules.users.domain.entities import User
from modules.users.domain.exceptions import UserNotFoundError
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from shared.utils.uuid_tools import uuid


@pytest.mark.asyncio
class TestGetUser:
    async def test_returns_user_when_user_exists(
        self, users_repo: UserRepositoryABC, user: User
    ):
        result = await GetUserHandler(users_repo).handle(GetUserCommand(id=user.id))

        assert result
        retrieved_user = result.unwrap_value()
        assert retrieved_user.username == user.username
        assert retrieved_user.fullname == user.fullname
        assert retrieved_user.email == user.email

    async def test_fails_when_user_does_not_exist(self, users_repo: UserRepositoryABC):
        result = await GetUserHandler(users_repo).handle(GetUserCommand(id=uuid()))

        assert not result
        assert isinstance(result.error, UserNotFoundError)
