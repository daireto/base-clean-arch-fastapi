from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware, correlation_id
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.utils import is_body_allowed_for_status_code
from starlette.responses import JSONResponse

from api.middlewares.access_log_middleware import AccessLogMiddleware
from config import settings
from logger import get_logger, global_app_logger, setup_log_rotation
from modules.resources.infrastructure.persistence.models.sqlite import (
    SQLiteResourcesBaseModel,
)
from modules.resources.presentation.api import router as resources_router
from shared.domain.exceptions import DomainError
from shared.infrastructure.db import init_db
from shared.presentation.api import router as shared_router

if settings.use_log_rotation:
    setup_log_rotation(
        loggers=[global_app_logger],
        filepath=settings.logs_path,
    )


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    global_app_logger.info('Starting app')
    base_models: list = [
        SQLiteResourcesBaseModel,
    ]
    try:
        conn = await init_db(base_models)
        global_app_logger.info(f'App started. Listening on port {settings.port}')
        global_app_logger.info(
            f'Documentation available at {settings.swagger_url} and {settings.redoc_url}'
        )
        yield
    except Exception as e:
        global_app_logger.error('Error initializing database', exc_info=e)
    else:
        await conn.close()
    global_app_logger.info('Stopping app')


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    debug=settings.debug,
)


# Routers
app.include_router(shared_router)
app.include_router(resources_router)


# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['X-Requested-With', 'X-Request-ID'],
    expose_headers=['X-Request-ID'],
)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(AccessLogMiddleware, logger=get_logger('access'))


# Exception handlers
def get_correlation_id_header() -> dict[str, str]:
    return {'X-Request-ID': correlation_id.get() or ''}


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> Response:
    headers = getattr(exc, 'headers', {}) or {}
    headers.update(get_correlation_id_header())
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return ORJSONResponse(
        {'detail': exc.detail}, status_code=exc.status_code, headers=headers
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return ORJSONResponse(
        content={'detail': exc.errors()},
        status_code=422,
        headers=get_correlation_id_header(),
    )


@app.exception_handler(DomainError)
async def domain_exception_handler(_: Request, exc: DomainError) -> Response:
    return ORJSONResponse(
        {'detail': exc.detail.model_dump()},
        status_code=exc.status_code,
        headers=get_correlation_id_header(),
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(_: Request, exc: Exception) -> Response:
    global_app_logger.error('Unexpected error', exc_info=exc)
    return ORJSONResponse(
        {'detail': 'Internal server error'},
        status_code=500,
        headers=get_correlation_id_header(),
    )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.port,
        log_config=None,
        reload=settings.is_dev,
    )
