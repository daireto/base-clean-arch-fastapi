import validators

from modules.resources.domain.errors import ResourceTypeNotSupportedError
from shared.domain.errors import InvalidURLError
from shared.domain.value_object import ValueObject


class ResourceType(ValueObject[str]):
    def validate(self) -> None:
        if self.value not in ['image', 'video', 'audio', 'text', 'other']:
            raise ResourceTypeNotSupportedError(self.value)


class ResourceUrl(ValueObject[str]):
    def validate(self) -> None:
        if not validators.url(self.value):
            raise InvalidURLError(self.value)
