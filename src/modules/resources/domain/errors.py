from enum import Enum
from uuid import UUID

from shared.domain.errors import InvalidInputError, NotFoundError


class ErrorCodes(str, Enum):
    RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND'
    RESOURCE_TYPE_NOT_SUPPORTED = 'RESOURCE_TYPE_NOT_SUPPORTED'


class ResourceNotFoundError(NotFoundError):
    def __init__(self, id_: UUID) -> None:
        self.id = id_
        super().__init__(
            message='Resource not found',
            error_code=ErrorCodes.RESOURCE_NOT_FOUND,
            resource_id=id_,
        )


class ResourceTypeNotSupportedError(InvalidInputError):
    def __init__(self, type_: str) -> None:
        self.type = type_
        super().__init__(
            message=(
                'Resource type not supported, must be one of:'
                ' image, video, audio, text, other'
            ),
            error_code=ErrorCodes.RESOURCE_TYPE_NOT_SUPPORTED,
            resource_type=type_,
        )
