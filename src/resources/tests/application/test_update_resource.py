import uuid

import pytest

from src.resources.application.update_resource import (
    UpdateResourceCommand,
    UpdateResourceHandler,
)
from src.resources.domain.entities import Resource
from src.resources.domain.errors import (
    InvalidURLError,
    ResourceNotFoundError,
    ResourceTypeNotSupportedError,
)
from src.resources.domain.value_objects import ResourceType, ResourceUrl
from src.resources.tests.application.mock_repository import MockResourcesRepository
from src.shared.domain.utils import empty_uuid


@pytest.mark.asyncio
class TestUpdateResource:
    async def test_update_resource(self):
        resource_repository = MockResourcesRepository()
        id_ = uuid.uuid4()
        resource_repository.resources[id_] = Resource(
            name='Random Image',
            url=ResourceUrl(value='https://example.com'),
            type=ResourceType(value='image'),
        )

        resource = await UpdateResourceHandler(resource_repository).handle(
            UpdateResourceCommand(
                id_=id_,
                name='Random Text',
                url='https://example.org',
                type='text',
            )
        )

        assert resource.id_ == id_
        assert resource.name == 'Random Text'
        assert resource.url == 'https://example.org'
        assert resource.type == 'text'

    async def test_raise_when_resource_url_is_invalid(self):
        resource_repository = MockResourcesRepository()
        id_ = uuid.uuid4()
        resource_repository.resources[id_] = Resource(
            name='Random Image',
            url=ResourceUrl(value='https://example.com'),
            type=ResourceType(value='image'),
        )

        with pytest.raises(InvalidURLError):
            await UpdateResourceHandler(resource_repository).handle(
                UpdateResourceCommand(
                    id_=id_,
                    name='Random Image',
                    url='not-a-valid-url',
                    type='image',
                )
            )
        resources = await resource_repository.all()

        assert len(resources) == 0

    async def test_raise_when_resource_type_is_not_supported(self):
        resource_repository = MockResourcesRepository()
        id_ = uuid.uuid4()
        resource_repository.resources[id_] = Resource(
            name='Random Image',
            url=ResourceUrl(value='https://example.com'),
            type=ResourceType(value='image'),
        )

        with pytest.raises(ResourceTypeNotSupportedError):
            await UpdateResourceHandler(resource_repository).handle(
                UpdateResourceCommand(
                    id_=id_,
                    name='Random Image',
                    url='https://example.com',
                    type='not-a-valid-type',
                )
            )
        resources = await resource_repository.all()

        assert len(resources) == 0

    async def test_raise_when_updating_resource_that_does_not_exist(self):
        resource_repository = MockResourcesRepository()

        with pytest.raises(ResourceNotFoundError):
            await UpdateResourceHandler(resource_repository).handle(
                UpdateResourceCommand(
                    id_=empty_uuid(),
                    name='Random Image',
                    url='https://example.com',
                    type='image',
                )
            )
