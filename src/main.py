from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqladmin import Admin

from api.config import settings
from api.exception_handlers import exception_handlers
from api.middlewares.access_log_middleware import AccessLogMiddleware
from logger import get_logger, global_app_logger, setup_log_rotation
from modules.resources.infrastructure.persistence.admin import ResourceAdmin
from modules.resources.infrastructure.persistence.models.sqlite import (
    BaseModel,
)
from modules.resources.presentation.api import router as resources_router
from shared.infrastructure.db import conn, init_db
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
        BaseModel,
    ]
    try:
        await init_db(base_models)
        global_app_logger.info(settings.startup_msg)
        yield
    except Exception as e:
        global_app_logger.error('Error initializing database', exc_info=e)
    else:
        await conn.close()
    global_app_logger.info('Stopping app')


app = FastAPI(
    debug=settings.debug,
    default_response_class=ORJSONResponse,
    exception_handlers=exception_handlers,
    lifespan=lifespan,
)

# Admin
admin = Admin(app, session_maker=conn.async_sessionmaker)
admin.add_view(ResourceAdmin)


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
app.add_middleware(
    AccessLogMiddleware,
    logger=get_logger('access'),
    excluded_path_prefixes=settings.access_log_excluded_path_prefixes,
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
