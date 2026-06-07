from typing import Self

from pydantic import Field, HttpUrl

from modules.resources.domain.enums import MediaType
from modules.resources.domain.value_objects import ResourceUrl
from shared.domain.bases.entity import Entity


class Resource(Entity):
    name: str = Field(min_length=5, max_length=255)
    url: ResourceUrl
    type: MediaType

    @property
    def url_value(self) -> str:
        return str(self.url.value)

    class Builder(Entity.Builder):
        def __init__(self) -> None:
            super().__init__()
            self._name = None
            self._url = None
            self._type = None

        def with_name(self, name: str) -> Self:
            self._name = name
            return self

        def with_url(self, url: str | HttpUrl) -> Self:
            self._url = url
            return self

        def with_type(self, type_: str | MediaType) -> Self:
            self._type = type_
            return self

        def build(self) -> 'Resource':
            return Resource.model_validate(
                {
                    'id': self._id,
                    'name': self._name,
                    'url': ResourceUrl(value=self._url) if self._url else None,  # type: ignore
                    'type': self._type,
                }
            )
