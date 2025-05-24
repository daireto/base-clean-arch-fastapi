from dataclasses import dataclass

import validators

from resources.domain.exceptions import InvalidURLError


@dataclass(frozen=True, kw_only=True)
class ResourceUrl:
    value: str

    def __post_init__(self):
        if not validators.url(self.value):
            raise InvalidURLError(self.value)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, value: 'ResourceUrl | str') -> bool:
        return (
            self.value == value.value
            if isinstance(value, ResourceUrl)
            else self.value == value
        )
