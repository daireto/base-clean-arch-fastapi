from asgi_correlation_id import correlation_id
from fastapi import HTTPException, Request, Response, status
from fastapi.responses import ORJSONResponse
from fastapi.utils import is_body_allowed_for_status_code

from shared.domain.errors import (
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


async def http_exception_handler(_: Request, exc: HTTPException) -> Response:
    headers = getattr(exc, 'headers', {}) or {}
    headers.update({'X-Request-ID': correlation_id.get() or ''})
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return ORJSONResponse(
        {'detail': exc.detail}, status_code=exc.status_code, headers=headers
    )
