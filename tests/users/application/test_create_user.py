import pytest
from odata_v4_query import ODataQueryOptions
from pydantic import SecretStr, ValidationError

from modules.users.application.use_cases.create_user import (
    CreateUserCommand,
    CreateUserHandler,
)
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)


@pytest.mark.asyncio
class TestCreateUser:
    async def test_returns_created_user(self, users_repo: UserRepositoryABC):
        await CreateUserHandler(users_repo).handle(
            CreateUserCommand(
                username='testuser1',
                fullname='Test User 1',
                email='testuser1@example.com',
                gender='male',
                password=SecretStr('password123'),
            )
        )
        users = await users_repo.all(
            odata_options=ODataQueryOptions(top=100),
        )

        assert len(users) == 1
        assert users[0].username == 'testuser1'

    async def test_raises_when_user_email_is_invalid(
        self, users_repo: UserRepositoryABC
    ):
        with pytest.raises(ValidationError):
            await CreateUserHandler(users_repo).handle(
                CreateUserCommand(
                    username='testuser1',
                    fullname='Test User 1',
                    email='not-a-valid-email',
                    gender='male',
                    password=SecretStr('password123'),
                )
            )

    async def test_raises_when_user_gender_is_not_supported(
        self, users_repo: UserRepositoryABC
    ):
        with pytest.raises(ValidationError):
            await CreateUserHandler(users_repo).handle(
                CreateUserCommand(
                    username='testuser1',
                    fullname='Test User 1',
                    email='testuser1@example.com',
                    gender='not-a-valid-gender',
                    password=SecretStr('password123'),
                )
            )
