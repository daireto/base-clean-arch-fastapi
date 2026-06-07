from collections.abc import AsyncGenerator

import pytest_asyncio

from modules.users.domain.entities import User
from modules.users.infrastructure.persistence.repositories.mock import (
    MockUserRepository,
)
from shared.utils.validation_types import HashedSecretStr


@pytest_asyncio.fixture
async def user(users_repo: MockUserRepository) -> AsyncGenerator[User]:
    user = await users_repo.create(
        User.Builder()
        .with_username('testuser1')
        .with_fullname('Test User 1')
        .with_email('testuser1@example.com')
        .with_gender('male')
        .with_role('user')
        .build(),
        password=HashedSecretStr('password123'),
    )
    yield user
    users_repo.clear()


@pytest_asyncio.fixture
async def users(
    users_repo: MockUserRepository,
) -> AsyncGenerator[list[User]]:
    users = [
        await users_repo.create(
            User.Builder()
            .with_username('testuser1')
            .with_fullname('Test User 1')
            .with_email('testuser1@example.com')
            .with_gender('male')
            .with_role('user')
            .build(),
            password=HashedSecretStr('password123'),
        ),
        await users_repo.create(
            User.Builder()
            .with_username('testuser2')
            .with_fullname('Test User 2')
            .with_email('testuser2@example.com')
            .with_gender('female')
            .with_role('admin')
            .build(),
            password=HashedSecretStr('password123'),
        ),
    ]
    yield users
    users_repo.clear()
