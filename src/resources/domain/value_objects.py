import validators

from resources.domain.errors import InvalidURLError, ResourceTypeNotSupportedError
from shared.domain.value_object import ValueObject


class ResourceType(ValueObject):
    value: str

    def validate(self) -> None:
        if self.value not in ['image', 'video', 'audio', 'text', 'other']:
            raise ResourceTypeNotSupportedError(self.value)


class ResourceUrl(ValueObject):
    value: str

    def validate(self) -> None:
        if not validators.url(self.value):
            raise InvalidURLError(self.value)
