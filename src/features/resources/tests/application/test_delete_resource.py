import pytest

from src.features.resources.application.use_cases.delete_resource import (
    DeleteResourceCommand,
    DeleteResourceHandler,
)
from src.features.resources.domain.entities import Resource
from src.features.resources.domain.errors import ResourceNotFoundError
from src.features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from src.shared.utils.uuid_tools import empty_uuid


@pytest.mark.asyncio
class TestDeleteResource:
    async def test_return_none_after_deleting_resource(
        self, repo: ResourceRepositoryABC, resource: Resource
    ):
        # Act
        await DeleteResourceHandler(repo).handle(DeleteResourceCommand(id=resource.id))
        resources_count = await repo.count()

        # Assert
        assert not resources_count

    async def test_fails_when_resource_does_not_exist(
        self, repo: ResourceRepositoryABC
    ):
        # Act
        result = await DeleteResourceHandler(repo).handle(
            DeleteResourceCommand(id=empty_uuid())
        )

        # Assert
        assert not result
        assert isinstance(result.error, ResourceNotFoundError)
