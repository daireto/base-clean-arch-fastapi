from resources.application.create_resource import CreateResource
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
        CreateResource(resource_repository).execute()
        assert len(resource_repository.all()) == 1
