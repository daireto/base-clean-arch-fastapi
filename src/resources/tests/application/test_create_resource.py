import pytest

from resources.application.create_resource import (
    CreateResource,
    CreateResourceCommand,
)
from resources.domain.exceptions import InvalidURL
from resources.domain.models import Resource
from resources.domain.repositories import ResourcesRepository


class FakeResourcesRepository(ResourcesRepository):
    def __init__(self):
        self.resources = []

    def all(self) -> list[Resource]:
        return self.resources

    def save(self, resource: Resource) -> None:
        self.resources.append(resource)


class TestCreateResource:
    def test_create_resource(self):
        resource_repository = FakeResourcesRepository()
        CreateResource(resource_repository).execute(
            CreateResourceCommand(resource_url='https://example.com')
        )
        resources = resource_repository.all()
        assert len(resources) == 1
        assert resources[0].url() == 'https://example.com'

    def test_raise_when_resource_url_is_invalid(self):
        resource_repository = FakeResourcesRepository()
        create_resource = CreateResource(resource_repository)
        with pytest.raises(InvalidURL):
            create_resource.execute(
                CreateResourceCommand(resource_url='not-a-valid-url')
            )
        resources = resource_repository.all()
        assert len(resources) == 0
