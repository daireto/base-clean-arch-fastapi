import pytest

from modules.resources.application.use_cases.delete_resource import (
    DeleteResourceCommand,
    DeleteResourceHandler,
)
from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from shared.utils.uuid_tools import uuid


@pytest.mark.asyncio
class TestDeleteResource:
    async def test_return_none_when_resource_exists(
        self, resources_repo: ResourceRepositoryABC, resource: Resource
    ):
        count_before = await resources_repo.count()

        result = await DeleteResourceHandler(resources_repo).handle(
            DeleteResourceCommand(id=resource.id)
        )

        assert result
        assert result.value is None
        assert await resources_repo.count() == count_before - 1

    async def test_returns_none_when_resource_does_not_exist(
        self, resources_repo: ResourceRepositoryABC
    ):
        count_before = await resources_repo.count()

        result = await DeleteResourceHandler(resources_repo).handle(
            DeleteResourceCommand(id=uuid())
        )

        assert result
        assert result.value is None
        assert await resources_repo.count() == count_before
