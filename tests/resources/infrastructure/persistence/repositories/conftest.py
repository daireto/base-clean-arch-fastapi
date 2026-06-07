from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlactive import DBConnection

from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from modules.resources.infrastructure.persistence.models.sqlite import (
    BaseModel,
    ResourceModel,
)
from modules.resources.infrastructure.persistence.repositories.sqlite import (
    SQLiteResourceRepository,
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
async def resources_repo(conn: DBConnection) -> ResourceRepositoryABC:
    return SQLiteResourceRepository(conn)


@pytest_asyncio.fixture
async def resource_model(resources_repo: ResourceRepositoryABC) -> ResourceModel:
    _ = resources_repo
    return await ResourceModel.from_entity(
        Resource.Builder()
        .with_name('Random Image')
        .with_url('https://example.com/')
        .with_type('image')
        .build()
    ).save()


@pytest_asyncio.fixture
async def resource_models(resources_repo: ResourceRepositoryABC) -> list[ResourceModel]:
    _ = resources_repo
    return [
        await ResourceModel.from_entity(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.com/')
            .with_type('image')
            .build()
        ).save(),
        await ResourceModel.from_entity(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.org/')
            .with_type('image')
            .build()
        ).save(),
    ]
