import logging
import time

from asgi_correlation_id.context import correlation_id
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from structlog.stdlib import BoundLogger


class AccessLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, logger: BoundLogger) -> None:
        super().__init__(app)
        self._logger = logger

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as e:
            await self.__access_log(
                request=request,
                duration_ms=(time.time() - start_time) * 1000,
                exception=e,
            )
            raise
        await self.__access_log(
            request=request,
            duration_ms=(time.time() - start_time) * 1000,
            response=response,
        )
        return response

    async def __access_log(
        self,
        request: Request,
        duration_ms: float,
        response: Response | None = None,
        exception: Exception | None = None,
    ) -> None:
        status_code = (
            response.status_code if response else status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        request_failed = exception or status_code >= status.HTTP_400_BAD_REQUEST
        self._logger.log(
            logging.ERROR if request_failed else logging.INFO,
            'Request failed' if request_failed else 'Request succeeded',
            request_id=correlation_id.get(),
            method=request.method,
            path=request.url.path,
            query=request.url.query,
            protocol=request.scope.get('scheme', 'http'),
            status_code=status_code,
            duration_ms=duration_ms,
            user_id=request.headers.get('x-user-id'),
            trace_id=request.headers.get('x-trace-id'),
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get('user-agent'),
            referrer=request.headers.get('referer'),
            exception=str(exception),
        )
