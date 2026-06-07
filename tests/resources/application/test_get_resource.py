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
from shared.utils.uuid_tools import uuid


@pytest.mark.asyncio
class TestGetResource:
    async def test_returns_resource_when_resource_exists(
        self, resources_repo: ResourceRepositoryABC, resource: Resource
    ):
        result = await GetResourceHandler(resources_repo).handle(
            GetResourceCommand(id=resource.id)
        )

        assert result
        resource = result.unwrap_value()
        assert resource.name == resource.name
        assert str(resource.url) == str(resource.url)
        assert resource.type == resource.type

    async def test_fails_when_resource_does_not_exist(
        self, resources_repo: ResourceRepositoryABC
    ):
        result = await GetResourceHandler(resources_repo).handle(
            GetResourceCommand(id=uuid())
        )

        assert not result
        assert isinstance(result.error, ResourceNotFoundError)
