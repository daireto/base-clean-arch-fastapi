from collections.abc import Generator

import pytest
import pytest_asyncio

from features.resources.di import deps
from features.resources.domain.entities import Resource
from features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from features.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)


@pytest.fixture
def repo() -> Generator[ResourceRepositoryABC]:
    with deps.override_for_test() as test_container:
        repo = MockResourceRepository()
        test_container[ResourceRepositoryABC] = repo
        yield repo


@pytest_asyncio.fixture
async def resource(repo: ResourceRepositoryABC) -> Resource:
    return await repo.create(
        Resource.Builder()
        .with_name('Random Image')
        .with_url('https://example.com')
        .with_type('image')
        .build()
    )


@pytest_asyncio.fixture
async def resources(repo: ResourceRepositoryABC) -> list[Resource]:
    return [
        await repo.create(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.com')
            .with_type('image')
            .build()
        ),
        await repo.create(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.org')
            .with_type('image')
            .build()
        ),
    ]
