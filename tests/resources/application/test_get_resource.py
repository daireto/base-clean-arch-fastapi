import pytest

from modules.resources.application.use_cases.get_resource import (
    GetResourceCommand,
    GetResourceHandler,
)
from modules.resources.domain.entities import Resource
from modules.resources.domain.exceptions import ResourceNotFoundError
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from shared.utils.uuid_tools import empty_uuid


@pytest.mark.asyncio
class TestGetResource:
    async def test_returns_resource_when_resource_exists(
        self, repo: ResourceRepositoryABC, resource: Resource
    ):
        result = await GetResourceHandler(repo).handle(
            GetResourceCommand(id=resource.id)
        )

        assert result
        resource = result.unwrap_value()
        assert resource.name == 'Random Image'
        assert str(resource.url) == 'https://example.com/'
        assert resource.type == 'image'

    async def test_fails_when_resource_does_not_exist(
        self, repo: ResourceRepositoryABC
    ):
        result = await GetResourceHandler(repo).handle(
            GetResourceCommand(id=empty_uuid())
        )

        assert not result
        assert isinstance(result.error, ResourceNotFoundError)
