import pytest
import pytest_asyncio
from pydantic import SecretStr

from modules.users.domain.entities import User
from modules.users.infrastructure.persistence.repositories.mock import (
    MockUserRepository,
)


@pytest.fixture
def users_repo() -> MockUserRepository:
    return MockUserRepository()


@pytest_asyncio.fixture
async def user(users_repo: MockUserRepository) -> User:
    return await users_repo.create(
        User.Builder()
        .with_username('testuser1')
        .with_fullname('Test User 1')
        .with_email('testuser1@example.com')
        .with_gender('male')
        .build(),
        password=SecretStr('password123'),
    )


@pytest_asyncio.fixture
async def users(users_repo: MockUserRepository) -> list[User]:
    return [
        await users_repo.create(
            User.Builder()
            .with_username('testuser1')
            .with_fullname('Test User 1')
            .with_email('testuser1@example.com')
            .with_gender('male')
            .build(),
            password=SecretStr('password123'),
        ),
        await users_repo.create(
            User.Builder()
            .with_username('testuser2')
            .with_fullname('Test User 2')
            .with_email('testuser2@example.com')
            .with_gender('female')
            .build(),
            password=SecretStr('password123'),
        ),
    ]
