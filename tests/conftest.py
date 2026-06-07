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

from core.app import create_app, register_middlewares
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from modules.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from modules.users.infrastructure.persistence.repositories.mock import (
    MockUserRepository,
)
from shared.application.instrumentation import (
    CreationUseCaseInstrumentation,
    DeletionUseCaseInstrumentation,
    ListingUseCaseInstrumentation,
    RetrievalUseCaseInstrumentation,
    UpdateUseCaseInstrumentation,
    UseCaseInstrumentation,
)


def get_use_case_instrumentation() -> UseCaseInstrumentation:
    return UseCaseInstrumentation()


provider = Provider(scope=Scope.APP)
provider.provide(MockResourceRepository, provides=ResourceRepositoryABC)
provider.provide(MockUserRepository, provides=UserRepositoryABC)
provider.provide(get_use_case_instrumentation, provides=CreationUseCaseInstrumentation)
provider.provide(get_use_case_instrumentation, provides=DeletionUseCaseInstrumentation)
provider.provide(get_use_case_instrumentation, provides=RetrievalUseCaseInstrumentation)
provider.provide(get_use_case_instrumentation, provides=ListingUseCaseInstrumentation)
provider.provide(get_use_case_instrumentation, provides=UpdateUseCaseInstrumentation)


@pytest_asyncio.fixture(scope='session')
async def container() -> AsyncGenerator[AsyncContainer]:
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
async def resources_repo(container: AsyncContainer) -> MockResourceRepository:
    return await container.get(ResourceRepositoryABC)  # type: ignore


@pytest_asyncio.fixture(scope='session')
async def users_repo(container: AsyncContainer) -> MockUserRepository:
    return await container.get(UserRepositoryABC)  # type: ignore
