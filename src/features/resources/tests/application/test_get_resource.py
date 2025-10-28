import pytest

from features.resources.application.use_cases.get_resource import (
    GetResourceCommand,
    GetResourceHandler,
)
from features.resources.domain.entities import Resource
from features.resources.domain.errors import ResourceNotFoundError
from features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from shared.utils.uuid_tools import empty_uuid


@pytest.mark.asyncio
class TestGetResource:
    async def test_returns_resource_details_after_getting_resource(
        self, repo: ResourceRepositoryABC, resource: Resource
    ):
        # Act
        result = await GetResourceHandler(repo).handle(
            GetResourceCommand(id=resource.id)
        )
        resource = result.get_value_or_raise()

        # Assert
        assert resource.name == 'Random Image'
        assert resource.url == 'https://example.com'
        assert resource.type == 'image'

    async def test_fails_when_resource_does_not_exist(
        self, repo: ResourceRepositoryABC
    ):
        # Act
        result = await GetResourceHandler(repo).handle(
            GetResourceCommand(id=empty_uuid())
        )

        # Assert
        assert not result
        assert isinstance(result.error, ResourceNotFoundError)
