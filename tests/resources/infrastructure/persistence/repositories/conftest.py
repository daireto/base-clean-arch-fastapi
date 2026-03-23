from collections.abc import AsyncGenerator, AsyncIterable

import pytest_asyncio
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from sqlactive import DBConnection

from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.infrastructure.persistence.models.sqlite import (
    BaseModel,
    ResourceModel,
)
from modules.resources.infrastructure.persistence.repositories.sqlite import (
    SQLiteResourceRepository,
)


class DBConnectionProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_db_connection(self) -> AsyncIterable[DBConnection]:
        mock_conn = DBConnection('sqlite+aiosqlite:///:memory:', echo=False)
        await mock_conn.init_db(BaseModel)

        yield mock_conn

        async with mock_conn.async_engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
        await mock_conn.close()


@pytest_asyncio.fixture
async def container() -> AsyncGenerator[AsyncContainer, None]:
    provider = Provider(scope=Scope.APP)
    provider.provide(SQLiteResourceRepository, provides=ResourceRepositoryABC)

    container = make_async_container(provider, DBConnectionProvider())
    yield container
    await container.close()


@pytest_asyncio.fixture
async def resource_model(repo: ResourceRepositoryABC) -> ResourceModel:
    _ = repo
    return await ResourceModel.from_entity(
        Resource.Builder()
        .with_name('Random Image')
        .with_url('https://example.com/')
        .with_type('image')
        .build()
    ).save()


@pytest_asyncio.fixture
async def resource_models(repo: ResourceRepositoryABC) -> list[ResourceModel]:
    _ = repo
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
