from pydantic import Field

from modules.resources.domain.value_objects import ResourceType, ResourceUrl
from shared.domain.entity import Entity


class Resource(Entity):
    name: str = Field(min_length=1, max_length=255)
    url: ResourceUrl
    type: ResourceType

    @property
    def url_value(self) -> str:
        return self.url.value

    @property
    def type_value(self) -> str:
        return self.type.value

    def set_name(self, name: str) -> None:
        self.name = name

    def set_url(self, url: str) -> None:
        self.url = ResourceUrl(value=url)

    def set_type(self, type_: str) -> None:
        self.type = ResourceType(value=type_)

    class Builder(Entity.Builder):
        def __init__(self) -> None:
            super().__init__()
            self._name = ''
            self._url = ''
            self._type = ''

        def with_name(self, name: str) -> 'Resource.Builder':
            self._name = name
            return self

        def with_url(self, url: str) -> 'Resource.Builder':
            self._url = url
            return self

        def with_type(self, type_: str) -> 'Resource.Builder':
            self._type = type_
            return self

        def build(self) -> 'Resource':
            return Resource(
                id=self._id,
                name=self._name,
                url=ResourceUrl(value=self._url),
                type=ResourceType(value=self._type),
            )

        def build_with_defaults(self) -> 'Resource':
            return Resource(
                id=self._id,
                name=self._name or 'unnamed',
                url=ResourceUrl(value=self._url or 'https://example.com'),
                type=ResourceType(value=self._type or 'other'),
            )
