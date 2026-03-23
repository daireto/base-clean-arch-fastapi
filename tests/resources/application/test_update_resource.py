import pytest
from pydantic import ValidationError

from modules.resources.application.use_cases.update_resource import (
    UpdateResourceCommand,
    UpdateResourceHandler,
)
from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
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
                url='https://example.org/',
                type='text',
            )
        )

        # Assert
        assert result
        updated = result.unwrap_value()
        assert updated.id == resource.id
        assert updated.name == 'Random Text'
        assert str(updated.url) == 'https://example.org/'
        assert updated.type == 'text'

    async def test_returns_resource_details_after_creating_resource_when_it_does_not_exist(
        self, repo: ResourceRepositoryABC
    ):
        # Act
        result = await UpdateResourceHandler(repo).handle(
            UpdateResourceCommand(
                id=empty_uuid(),
                name='Random Image',
                url='https://example.com/',
                type='image',
            )
        )

        # Assert
        assert result
        created = result.unwrap_value()
        assert created.id is not None
        assert created.name == 'Random Image'
        assert str(created.url) == 'https://example.com/'
        assert created.type == 'image'

    async def test_raises_when_resource_url_is_invalid(
        self,
        repo: ResourceRepositoryABC,
        resource: Resource,
    ):
        # Assert
        with pytest.raises(ValidationError):
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
        with pytest.raises(ValidationError):
            await UpdateResourceHandler(repo).handle(
                UpdateResourceCommand(
                    id=resource.id,
                    name='Random Image',
                    url='https://example.com/',
                    type='not-a-valid-type',
                )
            )
