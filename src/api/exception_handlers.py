from asgi_correlation_id import correlation_id
from fastapi import HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi.utils import is_body_allowed_for_status_code
from starlette.responses import JSONResponse

from logger import global_app_logger
from shared.domain.exceptions import DomainError


def get_correlation_id_header() -> dict[str, str]:
    return {'X-Request-ID': correlation_id.get() or ''}


async def http_exception_handler(_: Request, exc: HTTPException) -> Response:
    headers = getattr(exc, 'headers', {}) or {}
    headers.update(get_correlation_id_header())
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return ORJSONResponse(
        {'detail': exc.detail}, status_code=exc.status_code, headers=headers
    )


async def request_validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return ORJSONResponse(
        content={'detail': exc.errors()},
        status_code=422,
        headers=get_correlation_id_header(),
    )


async def domain_exception_handler(_: Request, exc: DomainError) -> Response:
    return ORJSONResponse(
        {'detail': exc.detail.model_dump()},
        status_code=exc.status_code,
        headers=get_correlation_id_header(),
    )


async def unexpected_exception_handler(_: Request, exc: Exception) -> Response:
    global_app_logger.error('Unexpected error', exc_info=exc)
    return ORJSONResponse(
        {'detail': 'Internal server error'},
        status_code=500,
        headers=get_correlation_id_header(),
    )


exception_handlers = {
    HTTPException: http_exception_handler,
    RequestValidationError: request_validation_exception_handler,
    DomainError: domain_exception_handler,
    Exception: unexpected_exception_handler,
}
