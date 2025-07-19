from uuid import UUID

import pytest

from resources.application.create_resource import (
    CreateResourceCommand,
    CreateResourceHandler,
)
from resources.domain.entities import Resource
from resources.domain.errors import InvalidURLError
from resources.domain.repositories import ResourceRepositoryABC


class FakeResourcesRepository(ResourceRepositoryABC):
    def __init__(self) -> None:
        self.resources = {}

    async def get_by_id(self, id_: UUID) -> Resource:
        return self.resources[id_]

    async def all(self) -> list[Resource]:
        return list(self.resources.values())

    async def save(self, resource: Resource) -> None:
        self.resources[resource.id] = resource


@pytest.mark.asyncio
class TestCreateResource:
    async def test_create_resource(self):
        resource_repository = FakeResourcesRepository()

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
        resource_repository = FakeResourcesRepository()

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
