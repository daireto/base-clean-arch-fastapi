from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
)
from dishka.integrations.fastapi import setup_dishka
from fastapi.testclient import TestClient

from app.app import create_app
from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)


@pytest_asyncio.fixture
async def container() -> AsyncGenerator[AsyncContainer, None]:
    provider = Provider(scope=Scope.APP)
    provider.provide(MockResourceRepository, provides=ResourceRepositoryABC)

    container = make_async_container(provider)
    yield container
    await container.close()


@pytest.fixture
def client(container: AsyncContainer) -> Generator[TestClient]:
    app = create_app()
    setup_dishka(container, app)
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def repo(container: AsyncContainer) -> ResourceRepositoryABC:
    return await container.get(ResourceRepositoryABC)


@pytest_asyncio.fixture
async def resource(repo: ResourceRepositoryABC) -> Resource:
    return await repo.create(
        Resource.Builder()
        .with_name('Random Image')
        .with_url('https://example.com/')
        .with_type('image')
        .build()
    )


@pytest_asyncio.fixture
async def resources(repo: ResourceRepositoryABC) -> list[Resource]:
    return [
        await repo.create(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.com/')
            .with_type('image')
            .build()
        ),
        await repo.create(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.org/')
            .with_type('image')
            .build()
        ),
    ]
