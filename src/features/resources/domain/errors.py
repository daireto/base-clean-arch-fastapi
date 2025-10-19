from uuid import UUID

from src.features.resources.domain.error_codes import ErrorCodes
from src.shared.domain.errors import InvalidInputError, NotFoundError


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
