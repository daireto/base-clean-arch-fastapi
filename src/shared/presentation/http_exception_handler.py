from asgi_correlation_id import correlation_id
from fastapi import Request, Response
from fastapi.responses import ORJSONResponse
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException


async def http_exception_handler(_: Request, exc: HTTPException) -> Response:
    headers = getattr(exc, 'headers', {}) or {}
    headers.update({'X-Request-ID': correlation_id.get() or ''})
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return ORJSONResponse(
        {'detail': exc.detail}, status_code=exc.status_code, headers=headers
    )
