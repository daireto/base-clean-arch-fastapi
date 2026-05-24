import pytest

from modules.resources.application.use_cases.delete_resource import (
    DeleteResourceCommand,
    DeleteResourceHandler,
)
from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from shared.utils.uuid_tools import empty_uuid


@pytest.mark.asyncio
class TestDeleteResource:
    async def test_return_none_when_resource_exists(
        self, repo: ResourceRepositoryABC, resource: Resource
    ):
        count_before = await repo.count()

        result = await DeleteResourceHandler(repo).handle(
            DeleteResourceCommand(id=resource.id)
        )

        assert result
        assert result.value is None
        assert await repo.count() == count_before - 1

    async def test_returns_none_when_resource_does_not_exist(
        self, repo: ResourceRepositoryABC
    ):
        count_before = await repo.count()

        result = await DeleteResourceHandler(repo).handle(
            DeleteResourceCommand(id=empty_uuid())
        )

        assert result
        assert result.value is None
        assert await repo.count() == count_before
