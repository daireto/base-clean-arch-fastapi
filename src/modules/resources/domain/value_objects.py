from pydantic.networks import HttpUrl

from shared.domain.bases.value_object import ValueObject


class ResourceUrl(ValueObject[HttpUrl]):
    @property
    def scheme(self) -> str:
        return self.value.scheme

    @property
    def domain(self) -> str:
        return self.value.host or ''

    def domain_equals_to(self, domain: str) -> bool:
        return domain.lower() in self.domain.lower()

    def scheme_equals_to(self, scheme: str) -> bool:
        return scheme.lower() == self.scheme.lower()
