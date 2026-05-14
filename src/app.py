from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import ORJSONResponse
from sqlactive import DBConnection
from sqladmin import Admin

from config import settings
from logger import get_logger, setup_app_logger
from middlewares.access_log_middleware import AccessLogMiddleware
from middlewares.rate_limit_middleware import RateLimitMiddleware
from modules.resources.di import provider as resources_provider
from modules.resources.infrastructure.persistence.admin import ResourceAdmin
from modules.resources.presentation.api import router as resources_router
from shared.di import DBConnectionProvider
from shared.presentation.api import router as shared_router
from shared.presentation.exception_handlers import exception_handlers


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
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=['*'],
    )
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(
        AccessLogMiddleware,
        logger=get_logger('access'),
        excluded_path_prefixes=settings.access_log_excluded_path_prefixes,
    )
    app.add_middleware(
        RateLimitMiddleware,
        limit_string=settings.rate_limit_string,
        storage_uri=settings.rate_limit_storage_uri.get_secret_value(),
    )

    if not settings.is_dev:
        app.add_middleware(HTTPSRedirectMiddleware)


async def register_admin(app: FastAPI, container: AsyncContainer) -> None:
    conn = await container.get(DBConnection)
    admin = Admin(app, session_maker=conn.async_sessionmaker)
    admin.add_view(ResourceAdmin)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.logger.info('Starting app')

    container: AsyncContainer | None = app.state.dishka_container

    if app.state.enable_admin and container is not None:
        await register_admin(app, container)

    app.state.logger.info(settings.startup_msg)

    yield

    app.state.logger.info('Stopping app')

    if container is not None:
        await container.close()

    app.state.logger.info('App stopped')


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings.debug,
        default_response_class=ORJSONResponse,
        exception_handlers=exception_handlers,
        lifespan=lifespan,
    )

    setup_app_logger(
        app=app,
        filepath=settings.logs_path if settings.use_log_rotation else None,
    )

    app.state.enable_admin = False
    app.state.dishka_container = None

    register_routers(app)
    register_middlewares(app)

    return app


def create_production_app() -> FastAPI:
    app = create_app()

    app.state.enable_admin = True

    container = make_async_container(
        resources_provider,
        DBConnectionProvider(
            logger=get_logger('db'),
            database_url=settings.database_url,
        ),
        FastapiProvider(),
    )
    setup_dishka(container, app)

    return app
