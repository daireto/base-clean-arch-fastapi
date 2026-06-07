import pytest
from pydantic import ValidationError

from modules.users.application.use_cases.update_user import (
    UpdateUserCommand,
    UpdateUserHandler,
)
from modules.users.domain.entities import User
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from shared.utils.uuid_tools import uuid
from shared.utils.validation_types import HashedSecretStr


@pytest.mark.asyncio
class TestUpdateUser:
    async def test_returns_updated_user_when_user_exists(
        self,
        users_repo: UserRepositoryABC,
        user: User,
    ):
        result = await UpdateUserHandler(users_repo).handle(
            UpdateUserCommand(
                id=user.id,
                username='testuser1',
                fullname='Test User',
                email='testuser1@example.com',
                gender='male',
                role='user',
            )
        )

        assert result
        updated = result.unwrap_value()
        assert updated.id == user.id
        assert updated.username == user.username
        assert updated.fullname == 'Test User'

    async def test_returns_created_user_when_user_does_not_exist(
        self, users_repo: UserRepositoryABC
    ):
        result = await UpdateUserHandler(users_repo).handle(
            UpdateUserCommand(
                id=uuid(),
                username='testuser2',
                fullname='Test User 2',
                email='testuser2@example.com',
                gender='female',
                role='user',
                password=HashedSecretStr('password123'),
            )
        )

        assert result
        created = result.unwrap_value()
        assert created.id is not None
        assert created.username == 'testuser2'
        assert created.fullname == 'Test User 2'
        assert created.email == 'testuser2@example.com'
        assert created.gender == 'female'

    async def test_raises_when_user_email_is_invalid(
        self,
        users_repo: UserRepositoryABC,
        user: User,
    ):
        with pytest.raises(ValidationError):
            await UpdateUserHandler(users_repo).handle(
                UpdateUserCommand(
                    id=user.id,
                    username='testuser1',
                    fullname='Test User',
                    email='not-a-valid-email',
                    gender='male',
                    role='user',
                )
            )

    async def test_raises_when_user_gender_is_not_supported(
        self,
        users_repo: UserRepositoryABC,
        user: User,
    ):
        with pytest.raises(ValidationError):
            await UpdateUserHandler(users_repo).handle(
                UpdateUserCommand(
                    id=user.id,
                    username='testuser1',
                    fullname='Test User',
                    email='testuser1@example.com',
                    gender='not-a-valid-gender',
                    role='user',
                )
            )

    async def test_raises_when_user_role_is_not_supported(
        self,
        users_repo: UserRepositoryABC,
        user: User,
    ):
        with pytest.raises(ValidationError):
            await UpdateUserHandler(users_repo).handle(
                UpdateUserCommand(
                    id=user.id,
                    username='testuser1',
                    fullname='Test User',
                    email='testuser1@example.com',
                    gender='male',
                    role='not-a-valid-role',
                )
            )
