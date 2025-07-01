from uuid import UUID

from fastapi import status

from shared.domain.bases import BaseError


class ResourceNotFoundError(BaseError, ValueError):
    def __init__(self, id_: UUID) -> None:
        self.id = id_
        super().__init__(f'resource not found: {id_!r}', status.HTTP_404_NOT_FOUND)


class ResourceTypeNotSupportedError(BaseError, ValueError):
    def __init__(self, type_: str) -> None:
        self.type = type_
        super().__init__(
            f'resource type not supported: {type_!r}'
            f', must be one of: image, video, audio, text, other'
        )


class InvalidURLError(BaseError, ValueError):
    def __init__(self, url: str) -> None:
        self.url = url
        super().__init__(f'invalid URL: {url!r}')
