import pytest

from src.resources.application.create_resource import (
    CreateResourceCommand,
    CreateResourceHandler,
)
from src.resources.domain.errors import InvalidURLError
from src.resources.infrastructure.repositories.mock import MockResourcesRepository


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
