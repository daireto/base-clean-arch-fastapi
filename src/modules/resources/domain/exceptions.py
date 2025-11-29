from uuid import UUID

from modules.resources.domain.error_codes import ErrorCodes
from shared.domain.exceptions import ErrorDetail, InvalidInputError, NotFoundError


class ResourceNotFoundError(NotFoundError):
    def __init__(self, id_: UUID) -> None:
        self.id = id_
        super().__init__(
            detail=ErrorDetail(
                code=ErrorCodes.RESOURCE_NOT_FOUND,
                message='Resource not found',
                extra={'resource_id': id_},
            ),
        )


class ResourceTypeNotSupportedError(InvalidInputError):
    def __init__(self, type_: str, supported_types: list[str]) -> None:
        self.type = type_
        super().__init__(
            detail=ErrorDetail(
                code=ErrorCodes.RESOURCE_TYPE_NOT_SUPPORTED,
                message=(
                    f'Resource type not supported,'
                    f' supported types are: {", ".join(supported_types)}'
                ),
                extra={'resource_type': type_},
            ),
        )
