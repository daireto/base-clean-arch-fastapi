from resources.domain.models import Resource
from resources.domain.repositories import ResourcesRepository


class PostgreSQLResourcesRepository(ResourcesRepository):
    def get(self) -> Resource:
        return None
