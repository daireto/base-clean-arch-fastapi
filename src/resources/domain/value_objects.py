from dataclasses import dataclass

import validators

from resources.domain.exceptions import InvalidURL


@dataclass(frozen=True, kw_only=True)
class ResourceUrl:
    value: str

    def __post_init__(self):
        if not validators.url(self.value):
            raise InvalidURL(self.value)
