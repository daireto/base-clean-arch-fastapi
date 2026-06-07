import pytest

from modules.users.application.use_cases.delete_user import (
    DeleteUserCommand,
    DeleteUserHandler,
)
from modules.users.domain.entities import User
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from shared.utils.uuid_tools import uuid


@pytest.mark.asyncio
class TestDeleteUser:
    async def test_return_none_when_user_exists(
        self, users_repo: UserRepositoryABC, user: User
    ):
        count_before = await users_repo.count()

        result = await DeleteUserHandler(users_repo).handle(
            DeleteUserCommand(id=user.id)
        )

        assert result
        assert result.value is None
        assert await users_repo.count() == count_before - 1

    async def test_returns_none_when_user_does_not_exist(
        self, users_repo: UserRepositoryABC
    ):
        count_before = await users_repo.count()

        result = await DeleteUserHandler(users_repo).handle(
            DeleteUserCommand(id=uuid())
        )

        assert result
        assert result.value is None
        assert await users_repo.count() == count_before
