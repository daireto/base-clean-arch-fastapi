from urllib.parse import urlparse

import validators

from modules.resources.domain.exceptions import ResourceTypeNotSupportedError
from shared.domain.bases.value_object import ValueObject
from shared.domain.exceptions import InvalidURLError


class ResourceType(ValueObject[str]):
    def validate(self) -> None:
        supported_types = ['image', 'video', 'audio', 'text', 'other']
        if self.value not in supported_types:
            raise ResourceTypeNotSupportedError(self.value, supported_types)


class ResourceUrl(ValueObject[str]):
    def validate(self) -> None:
        if not validators.url(self.value):
            raise InvalidURLError(self.value)

    def get_scheme(self) -> str:
        return self.value.split('://')[0]

    def get_domain(self) -> str:
        return urlparse(self.value).netloc

    def domain_equals_to(self, domain: str) -> bool:
        return domain.lower() in self.get_domain().lower()

    def scheme_equals_to(self, scheme: str) -> bool:
        return scheme.lower() == self.get_scheme().lower()
