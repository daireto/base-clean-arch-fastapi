from resources.domain.value_objects import ResourceType, ResourceUrl
from shared.domain.entity import Entity


class Resource(Entity):
    name: str
    url: ResourceUrl
    type: ResourceType

    @property
    def url_value(self) -> str:
        return self.url.value

    @property
    def type_value(self) -> str:
        return self.type.value
