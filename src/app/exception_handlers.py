from asgi_correlation_id import correlation_id
from fastapi import HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi.utils import is_body_allowed_for_status_code
from pydantic import ValidationError
from starlette.responses import JSONResponse

from app.logger import global_app_logger
from shared.domain.bases.error import Error, ValidationErrorDetail
from shared.domain.error_codes import ErrorCode


def get_correlation_id_header() -> dict[str, str]:
    return {'X-Request-ID': correlation_id.get() or ''}


def get_correlation_id_urn() -> str | None:
    if req_id := correlation_id.get():
        return f'urn:uuid:{req_id}'
    return None


def build_rfc_9457_response_body(
    title: str,
    status: int,
    detail: str,
    code: str,
    type_: str = 'about:blank',
    errors: list[ValidationErrorDetail] | None = None,
) -> dict[str, object]:
    return {
        'type': type_,
        'title': title,
        'status': status,
        'detail': detail,
        'instance': get_correlation_id_urn(),
        'code': code,
        'errors': errors,
    }


async def http_exception_handler(_: Request, exc: HTTPException) -> Response:
    headers = getattr(exc, 'headers', {}) or {}
    headers.update(get_correlation_id_header())
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return ORJSONResponse(
        build_rfc_9457_response_body(
            title=exc.detail,
            status=exc.status_code,
            detail=exc.detail,
            code=ErrorCode.UNEXPECTED_ERROR,
        ),
        status_code=exc.status_code,
        headers=headers,
    )


async def request_validation_exception_handler(
    _: Request, exc: RequestValidationError | ValidationError
) -> JSONResponse:
    return ORJSONResponse(
        content=build_rfc_9457_response_body(
            title='Validation Error',
            status=422,
            detail='Invalid input.',
            code=ErrorCode.VALIDATION_ERROR,
            errors=ValidationErrorDetail.from_pydantic_error_details(exc.errors()),  # type: ignore
        ),
        status_code=422,
        headers=get_correlation_id_header(),
    )


async def domain_exception_handler(_: Request, exc: Error) -> Response:
    # TODO: Should i log here and the rest of the handlers?
    return ORJSONResponse(
        exc.to_rfc_9457_dict(instance=get_correlation_id_urn()),
        status_code=exc.status,
        headers=get_correlation_id_header(),
    )


async def unexpected_exception_handler(_: Request, exc: Exception) -> Response:
    global_app_logger.error('Unexpected error', exc_info=exc)
    return ORJSONResponse(
        build_rfc_9457_response_body(
            title='Internal Server Error',
            status=500,
            detail='An unexpected error occurred. Please try again later.',
            code=ErrorCode.UNEXPECTED_ERROR,
        ),
        status_code=500,
        headers=get_correlation_id_header(),
    )


exception_handlers = {
    HTTPException: http_exception_handler,
    RequestValidationError: request_validation_exception_handler,
    ValidationError: request_validation_exception_handler,  # TODO: Do i need this?
    Error: domain_exception_handler,
    Exception: unexpected_exception_handler,
}
