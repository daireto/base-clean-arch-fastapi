import pytest

from src.features.resources.application.use_cases.delete_resource import (
    DeleteResourceCommand,
    DeleteResourceHandler,
)
from src.features.resources.domain.entities import Resource
from src.features.resources.domain.errors import ResourceNotFoundError
from src.features.resources.domain.value_objects import ResourceType, ResourceUrl
from src.features.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)
from src.shared.utils import empty_uuid


@pytest.mark.asyncio
class TestDeleteResource:
    async def test_return_none_after_deleting_resource(self):
        # Arrange
        repo = MockResourceRepository()
        resource = await repo.create(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            )
        )

        # Act
        await DeleteResourceHandler(repo).handle(DeleteResourceCommand(id=resource.id))
        resources_count = await repo.count()

        # Assert
        assert not resources_count

    async def test_fails_when_resource_does_not_exist(self):
        # Arrange
        repo = MockResourceRepository()

        # Act
        result = await DeleteResourceHandler(repo).handle(
            DeleteResourceCommand(id=empty_uuid())
        )

        # Assert
        assert not result
        assert isinstance(result.error, ResourceNotFoundError)
