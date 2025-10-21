import pytest

from src.features.resources.application.use_cases.get_resource import (
    GetResourceCommand,
    GetResourceHandler,
)
from src.features.resources.domain.entities import Resource
from src.features.resources.domain.errors import ResourceNotFoundError
from src.features.resources.domain.value_objects import ResourceType, ResourceUrl
from src.features.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)
from src.shared.utils.uuid_tools import empty_uuid


@pytest.mark.asyncio
class TestGetResource:
    async def test_returns_resource_details_after_getting_resource(self):
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
        result = await GetResourceHandler(repo).handle(
            GetResourceCommand(id=resource.id)
        )
        resource = result.get_value_or_raise()

        # Assert
        assert resource.name == 'Random Image'
        assert resource.url == 'https://example.com'
        assert resource.type == 'image'

    async def test_fails_when_resource_does_not_exist(self):
        # Arrange
        repo = MockResourceRepository()

        # Act
        result = await GetResourceHandler(repo).handle(
            GetResourceCommand(id=empty_uuid())
        )

        # Assert
        assert not result
        assert isinstance(result.error, ResourceNotFoundError)
