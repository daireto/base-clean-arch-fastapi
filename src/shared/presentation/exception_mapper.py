from fastapi import HTTPException, status

from src.shared.domain.errors import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    DomainError,
    InvalidInputError,
    NotFoundError,
)

_exception_mapper: dict[type[DomainError], int] = {
    AuthenticationError: status.HTTP_401_UNAUTHORIZED,
    AuthorizationError: status.HTTP_403_FORBIDDEN,
    ConflictError: status.HTTP_409_CONFLICT,
    InvalidInputError: status.HTTP_400_BAD_REQUEST,
    NotFoundError: status.HTTP_404_NOT_FOUND,
}


def to_http_exception(error: Exception) -> HTTPException:
    if not isinstance(error, DomainError):
        return HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error))
    for error_class, status_code in _exception_mapper.items():
        if isinstance(error, error_class):
            detail = {
                'message': error.message,
                'code': error.error_code,
                'input': error.input_info,
            }
            return HTTPException(status_code=status_code, detail=detail)
    return HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(error))
