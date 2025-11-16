import pytest

from modules.resources.application.use_cases.update_resource import (
    UpdateResourceCommand,
    UpdateResourceHandler,
)
from modules.resources.domain.entities import Resource
from modules.resources.domain.exceptions import (
    ResourceNotFoundError,
    ResourceTypeNotSupportedError,
)
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from shared.domain.exceptions import InvalidURLError
from shared.utils.uuid_tools import empty_uuid


@pytest.mark.asyncio
class TestUpdateResource:
    async def test_returns_resource_details_after_updating_resource(
        self,
        repo: ResourceRepositoryABC,
        resource: Resource,
    ):
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

    async def test_raises_when_resource_url_is_invalid(
        self,
        repo: ResourceRepositoryABC,
        resource: Resource,
    ):
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

    async def test_raises_when_resource_type_is_not_supported(
        self,
        repo: ResourceRepositoryABC,
        resource: Resource,
    ):
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

    async def test_fails_when_resource_does_not_exist(
        self, repo: ResourceRepositoryABC
    ):
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
