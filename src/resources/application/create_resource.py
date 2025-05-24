from dataclasses import dataclass

from resources.domain.models import Resource
from resources.domain.repositories import ResourcesRepository
from resources.domain.value_objects import ResourceUrl


@dataclass
class CreateResourceDTO:
    resource_url: str


class CreateResource:
    def __init__(self, resource_repository: ResourcesRepository):
        self._resource_repository = resource_repository

    def execute(self, dto: CreateResourceDTO) -> None:
        resource_url = ResourceUrl(value=dto.resource_url)
        resource = Resource.create(resource_url)
        self._resource_repository.save(resource)
