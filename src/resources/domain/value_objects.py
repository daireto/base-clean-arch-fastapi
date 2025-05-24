from dataclasses import dataclass

import validators

from resources.domain.exceptions import InvalidURLError


@dataclass(frozen=True, kw_only=True)
class ResourceUrl:
    value: str

    def __post_init__(self):
        if not validators.url(self.value):
            raise InvalidURLError(self.value)
