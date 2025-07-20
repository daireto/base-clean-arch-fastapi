import uuid

import pytest

from src.resources.application.get_resource import (
    GetResourceCommand,
    GetResourceHandler,
)
from src.resources.domain.entities import Resource
from src.resources.domain.errors import ResourceNotFoundError
from src.resources.domain.value_objects import ResourceType, ResourceUrl
from src.resources.tests.application.mock_repository import MockResourcesRepository
from src.shared.domain.utils import empty_uuid


@pytest.mark.asyncio
class TestGetResource:
    async def test_get_resource_by_id(self):
        resource_repository = MockResourcesRepository()
        id_ = uuid.uuid4()
        resource_repository.resources = {
            id_: Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            )
        }

        resource = await GetResourceHandler(resource_repository).handle(
            GetResourceCommand(id_=id_)
        )

        assert resource.name == 'Random Image'
        assert resource.url == 'https://example.com'
        assert resource.type == 'image'

    async def test_raise_when_getting_a_resource_that_does_not_exist(self):
        resource_repository = MockResourcesRepository()

        with pytest.raises(ResourceNotFoundError):
            await GetResourceHandler(resource_repository).handle(
                GetResourceCommand(id_=empty_uuid())
            )
