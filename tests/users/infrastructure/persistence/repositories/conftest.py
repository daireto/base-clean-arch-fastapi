from collections.abc import AsyncGenerator

import pytest_asyncio
from pydantic import SecretStr
from sqlactive import DBConnection

from modules.users.domain.entities import User
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from modules.users.infrastructure.persistence.models.sqlite import (
    BaseModel,
    UserModel,
)
from modules.users.infrastructure.persistence.repositories.sqlite import (
    SQLiteUserRepository,
)


@pytest_asyncio.fixture
async def conn() -> AsyncGenerator[DBConnection]:
    mock_conn = DBConnection('sqlite+aiosqlite:///:memory:', echo=False)
    await mock_conn.init_db(BaseModel)

    yield mock_conn

    async with mock_conn.async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
    await mock_conn.close()


@pytest_asyncio.fixture
async def users_repo(conn: DBConnection) -> UserRepositoryABC:
    return SQLiteUserRepository(conn)


@pytest_asyncio.fixture
async def user_model(users_repo: UserRepositoryABC) -> UserModel:
    _ = users_repo
    return await UserModel.from_entity(
        User.Builder()
        .with_username('testuser1')
        .with_fullname('Test User 1')
        .with_email('testuser1@example.com')
        .with_gender('male')
        .build(),
        password=SecretStr('password123'),
    ).save()


@pytest_asyncio.fixture
async def user_models(users_repo: UserRepositoryABC) -> list[UserModel]:
    _ = users_repo
    return [
        await UserModel.from_entity(
            User.Builder()
            .with_username('testuser1')
            .with_fullname('Test User 1')
            .with_email('testuser1@example.com')
            .with_gender('male')
            .build(),
            password=SecretStr('password123'),
        ).save(),
        await UserModel.from_entity(
            User.Builder()
            .with_username('testuser2')
            .with_fullname('Test User 2')
            .with_email('testuser2@example.com')
            .with_gender('female')
            .build(),
            password=SecretStr('password123'),
        ).save(),
    ]
