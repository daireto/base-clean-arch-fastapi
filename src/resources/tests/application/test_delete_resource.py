import uuid

import pytest

from src.resources.application.delete_resource import (
    DeleteResourceCommand,
    DeleteResourceHandler,
)
from src.resources.domain.entities import Resource
from src.resources.domain.errors import ResourceNotFoundError
from src.resources.domain.value_objects import ResourceType, ResourceUrl
from src.resources.tests.application.mock_repository import MockResourcesRepository
from src.shared.domain.utils import empty_uuid


@pytest.mark.asyncio
class TestDeleteResource:
    async def test_delete_resource_by_id(self):
        resource_repository = MockResourcesRepository()
        id_ = uuid.uuid4()
        resource_repository.resources[id_] = Resource(
            name='Random Image',
            url=ResourceUrl(value='https://example.com'),
            type=ResourceType(value='image'),
        )

        await DeleteResourceHandler(resource_repository).handle(
            DeleteResourceCommand(id_=id_)
        )

        assert len(resource_repository.resources) == 0

    async def test_raise_when_deleting_a_resource_that_does_not_exist(self):
        resource_repository = MockResourcesRepository()

        with pytest.raises(ResourceNotFoundError):
            await DeleteResourceHandler(resource_repository).handle(
                DeleteResourceCommand(id_=empty_uuid())
            )
