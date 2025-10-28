from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from core.config import settings
from core.logger import get_logger, global_app_logger, setup_log_rotation
from middlewares.access_log import AccessLogMiddleware
from modules.resources.infrastructure.persistence.models.sqlite import (
    SQLiteResourcesBaseModel,
)
from modules.resources.presentation.api import router as resources_router
from shared.domain.errors import DomainError
from shared.infrastructure.db import init_db
from shared.presentation.api import router as shared_router
from shared.presentation.exception_handling import (
    http_exception_handler,
    to_http_exception,
)

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
@app.exception_handler(HTTPException)
async def http_exception_handler_with_correlation_id(
    request: Request, exc: HTTPException
) -> Response:
    return await http_exception_handler(request, exc)


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> Response:
    return await http_exception_handler(request, to_http_exception(exc))


@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception) -> Response:
    global_app_logger.error('Unhandled error', exc_info=exc)
    return await http_exception_handler(
        request, HTTPException(500, 'Internal server error')
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
