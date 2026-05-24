from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
)
from fastapi.testclient import TestClient

from app import create_app, register_middlewares
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from modules.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)


@pytest_asyncio.fixture(scope='session')
async def container() -> AsyncGenerator[AsyncContainer]:
    provider = Provider(scope=Scope.APP)
    provider.provide(MockResourceRepository, provides=ResourceRepositoryABC)

    container = make_async_container(provider)
    yield container
    await container.close()


@pytest.fixture(scope='session')
def client(container: AsyncContainer) -> Generator[TestClient]:
    app = create_app(container)

    register_middlewares(app, include_rate_limit=False)

    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture(scope='session')
async def repo(container: AsyncContainer) -> MockResourceRepository:
    return await container.get(ResourceRepositoryABC)  # type: ignore
