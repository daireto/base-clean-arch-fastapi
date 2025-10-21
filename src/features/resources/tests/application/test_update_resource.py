import pytest

from src.features.resources.application.use_cases.update_resource import (
    UpdateResourceCommand,
    UpdateResourceHandler,
)
from src.features.resources.domain.entities import Resource
from src.features.resources.domain.errors import (
    ResourceNotFoundError,
    ResourceTypeNotSupportedError,
)
from src.features.resources.domain.value_objects import ResourceType, ResourceUrl
from src.features.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)
from src.shared.domain.errors import InvalidURLError
from src.shared.utils.uuid_tools import empty_uuid


@pytest.mark.asyncio
class TestUpdateResource:
    async def test_returns_resource_details_after_updating_resource(self):
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
        result = await UpdateResourceHandler(repo).handle(
            UpdateResourceCommand(
                id=resource.id,
                name='Random Text',
                url='https://example.org',
                type='text',
            )
        )
        updated = result.get_value_or_raise()

        # Assert
        assert updated.id == resource.id
        assert updated.name == 'Random Text'
        assert updated.url == 'https://example.org'
        assert updated.type == 'text'

    async def test_raises_when_resource_url_is_invalid(self):
        # Arrange
        repo = MockResourceRepository()
        resource = await repo.create(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            )
        )

        # Assert
        with pytest.raises(InvalidURLError):
            await UpdateResourceHandler(repo).handle(
                UpdateResourceCommand(
                    id=resource.id,
                    name='Random Image',
                    url='not-a-valid-url',
                    type='image',
                )
            )

    async def test_raises_when_resource_type_is_not_supported(self):
        # Arrange
        repo = MockResourceRepository()
        resource = await repo.create(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            )
        )

        # Assert
        with pytest.raises(ResourceTypeNotSupportedError):
            await UpdateResourceHandler(repo).handle(
                UpdateResourceCommand(
                    id=resource.id,
                    name='Random Image',
                    url='https://example.com',
                    type='not-a-valid-type',
                )
            )

    async def test_fails_when_resource_does_not_exist(self):
        # Arrange
        repo = MockResourceRepository()

        # Act
        result = await UpdateResourceHandler(repo).handle(
            UpdateResourceCommand(
                id=empty_uuid(),
                name='Random Image',
                url='https://example.com',
                type='image',
            )
        )

        # Assert
        assert not result
        assert isinstance(result.error, ResourceNotFoundError)
