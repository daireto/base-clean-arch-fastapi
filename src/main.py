import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlactive import DBConnection
from sqladmin import Admin

from app.config import settings
from app.exception_handlers import exception_handlers
from app.middlewares.access_log_middleware import AccessLogMiddleware
from logger import get_logger, global_app_logger, setup_log_rotation
from modules.resources.di import provider as resources_provider
from modules.resources.infrastructure.persistence.admin import ResourceAdmin
from modules.resources.presentation.api import router as resources_router
from shared.di import DBConnectionProvider
from shared.presentation.api import router as shared_router

if settings.use_log_rotation:
    setup_log_rotation(
        loggers=[global_app_logger],
        filepath=settings.logs_path,
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global_app_logger.info('Starting app')
    global_app_logger.info(settings.startup_msg)

    yield

    await app.state.dishka_container.close()
    global_app_logger.info('Stopping app')


def register_routers(app: FastAPI) -> None:
    app.include_router(shared_router)
    app.include_router(resources_router)


def register_middlewares(app: FastAPI) -> None:
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


def register_admin(app: FastAPI, container: AsyncContainer) -> None:
    conn = asyncio.run(container.get(DBConnection))
    admin = Admin(app, session_maker=conn.async_sessionmaker)
    admin.add_view(ResourceAdmin)


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings.debug,
        default_response_class=ORJSONResponse,
        exception_handlers=exception_handlers,
        lifespan=lifespan,
    )

    register_routers(app)
    register_middlewares(app)

    return app


def create_production_app() -> FastAPI:
    app = create_app()

    container = make_async_container(
        resources_provider,
        DBConnectionProvider(),
        FastapiProvider(),
    )
    setup_dishka(container, app)

    register_admin(app, container)

    return app


app = create_production_app()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.port,
        log_config=None,
        reload=settings.is_dev,
    )
