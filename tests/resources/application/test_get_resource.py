import pytest

from modules.resources.application.use_cases.get_resource import (
    GetResourceCommand,
    GetResourceHandler,
)
from modules.resources.domain.entities import Resource
from modules.resources.domain.exceptions import ResourceNotFoundError
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
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

        # Assert
        assert result
        resource = result.unwrap_value()
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
