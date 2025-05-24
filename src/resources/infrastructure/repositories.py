from resources.domain.models import Resource
from resources.domain.repositories import ResourcesRepository


class SQLModelResourcesRepository(ResourcesRepository):
    def all(self) -> list[Resource]:
        pass

    def save(self, resource: Resource) -> None:
        pass
