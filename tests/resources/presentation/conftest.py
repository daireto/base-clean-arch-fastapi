from collections.abc import AsyncGenerator

import pytest_asyncio

from modules.resources.domain.entities import Resource
from modules.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)


@pytest_asyncio.fixture
async def resource(repo: MockResourceRepository) -> AsyncGenerator[Resource]:
    resource = await repo.create(
        Resource.Builder()
        .with_name('Random Image')
        .with_url('https://example.com/')
        .with_type('image')
        .build()
    )
    yield resource
    repo.clear()


@pytest_asyncio.fixture
async def resources(repo: MockResourceRepository) -> AsyncGenerator[list[Resource]]:
    resources = [
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
    yield resources
    repo.clear()
