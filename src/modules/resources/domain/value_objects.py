from pydantic.networks import HttpUrl

from modules.resources.domain.enums import MediaType
from shared.domain.bases.value_object import ValueObject


class ResourceType(ValueObject[MediaType]):
    pass


class ResourceUrl(ValueObject[HttpUrl]):
    def get_scheme(self) -> str:
        return self.value.scheme

    def get_domain(self) -> str:
        return self.value.host or ''

    def domain_equals_to(self, domain: str) -> bool:
        return domain.lower() in self.get_domain().lower()

    def scheme_equals_to(self, scheme: str) -> bool:
        return scheme.lower() == self.get_scheme().lower()
