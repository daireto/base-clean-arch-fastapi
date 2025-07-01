from dataclasses import dataclass

import validators

from resources.domain.errors import InvalidURLError, ResourceTypeNotSupportedError
from shared.domain.value_object import ValueObject


@dataclass(frozen=True, kw_only=True)
class ResourceType(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if self.value not in ['image', 'video', 'audio', 'text', 'other']:
            raise ResourceTypeNotSupportedError(self.value)


@dataclass(frozen=True, kw_only=True)
class ResourceUrl(ValueObject):
    value: str

    def __post_init__(self) -> None:
        if not validators.url(self.value):
            raise InvalidURLError(self.value)
