from src.features.resources.domain.value_objects import ResourceType, ResourceUrl
from src.shared.domain.entity import Entity


class Resource(Entity):
    name: str
    url: ResourceUrl
    type: ResourceType

    @property
    def url_value(self) -> str:
        return self.url.get_value()

    @property
    def type_value(self) -> str:
        return self.type.get_value()
