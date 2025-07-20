import pytest

from src.resources.application.create_resource import (
    CreateResourceCommand,
    CreateResourceHandler,
)
from src.resources.domain.errors import InvalidURLError, ResourceTypeNotSupportedError
from src.resources.tests.application.mock import MockResourcesRepository


@pytest.mark.asyncio
class TestCreateResource:
    async def test_create_resource(self):
        resource_repository = MockResourcesRepository()

        await CreateResourceHandler(resource_repository).handle(
            CreateResourceCommand(
                name='Random Image',
                url='https://example.com',
                type='image',
            )
        )
        resources = await resource_repository.all()

        assert len(resources) == 1
        assert resources[0].url == 'https://example.com'

    async def test_raise_when_resource_url_is_invalid(self):
        resource_repository = MockResourcesRepository()

        with pytest.raises(InvalidURLError):
            await CreateResourceHandler(resource_repository).handle(
                CreateResourceCommand(
                    name='Random Image',
                    url='not-a-valid-url',
                    type='image',
                )
            )
        resources = await resource_repository.all()

        assert len(resources) == 0

    async def test_raise_when_resource_type_is_not_supported(self):
        resource_repository = MockResourcesRepository()

        with pytest.raises(ResourceTypeNotSupportedError):
            await CreateResourceHandler(resource_repository).handle(
                CreateResourceCommand(
                    name='Random Image',
                    url='https://example.com',
                    type='not-a-valid-type',
                )
            )
        resources = await resource_repository.all()

        assert len(resources) == 0
