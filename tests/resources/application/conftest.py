import pytest
import pytest_asyncio

from modules.resources.domain.entities import Resource
from modules.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)


@pytest.fixture
def resources_repo() -> MockResourceRepository:
    return MockResourceRepository()


@pytest_asyncio.fixture
async def resource(resources_repo: MockResourceRepository) -> Resource:
    return await resources_repo.create(
        Resource.Builder()
        .with_name('Random Image')
        .with_url('https://example.com/')
        .with_type('image')
        .build()
    )


@pytest_asyncio.fixture
async def resources(resources_repo: MockResourceRepository) -> list[Resource]:
    return [
        await resources_repo.create(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.com/')
            .with_type('image')
            .build()
        ),
        await resources_repo.create(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.org/')
            .with_type('image')
            .build()
        ),
    ]
