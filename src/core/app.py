from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlactive import DBConnection
from sqladmin import Admin

from core.config import settings
from core.exception_handlers import exception_handlers
from core.logger import get_app_logger, get_logger, setup_app_logger
from core.middlewares.access_log_middleware import AccessLogMiddleware
from core.middlewares.rate_limit_middleware import RateLimitMiddleware
from core.middlewares.security_headers_middleware import SecurityHeadersMiddleware
from modules.resources.di import provider as resources_provider
from modules.resources.infrastructure.persistence.admin import ResourceAdmin
from modules.resources.presentation.api import router as resources_router
from modules.users.di import provider as users_provider
from modules.users.infrastructure.persistence.admin import UserAdmin
from modules.users.presentation.api import router as users_router
from shared.di import DBConnectionProvider
from shared.presentation.api import router as shared_router


def register_routers(app: FastAPI) -> None:
    app.include_router(shared_router)
    app.include_router(resources_router)
    app.include_router(users_router)


def register_middlewares(app: FastAPI, include_rate_limit: bool = True) -> None:
    app.add_middleware(
        SecurityHeadersMiddleware,
        hsts=settings.server.https,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.allow_origins.split(','),
        allow_methods=settings.cors.allow_methods.split(','),
        allow_headers=settings.cors.allow_headers.split(','),
        expose_headers=settings.cors.expose_headers.split(','),
    )
    app.add_middleware(
        AccessLogMiddleware,
        logger=get_logger('access'),
        excluded_path_prefixes=settings.log.access_log_excluded_path_prefixes,
    )
    app.add_middleware(CorrelationIdMiddleware)

    if settings.server.https:
        app.add_middleware(HTTPSRedirectMiddleware)

    if include_rate_limit:
        app.add_middleware(
            RateLimitMiddleware,
            storage_uri=settings.rate_limit.storage_uri.get_secret_value(),
            root_limit=settings.rate_limit.root_limit,
        )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.server.allowed_hosts.split(','),
    )


async def register_admin(app: FastAPI, container: AsyncContainer) -> None:
    conn = await container.get(DBConnection)
    admin = Admin(app, session_maker=conn.async_sessionmaker)
    admin.add_view(ResourceAdmin)
    admin.add_view(UserAdmin)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.logger.info('Starting app')

    container: AsyncContainer | None = app.state.dishka_container

    if app.state.register_admin and container is not None:
        await register_admin(app, container)

    app.state.logger.info(settings.startup_msg)

    yield

    app.state.logger.info('Stopping app')

    if container is not None:
        await container.close()

    app.state.logger.info('App stopped')


def create_app(
    container: AsyncContainer,
    logs_filepath: str | None = None,
    enable_admin: bool = False,
) -> FastAPI:
    app = FastAPI(
        debug=settings.server.debug,
        exception_handlers=exception_handlers,
        lifespan=lifespan,
    )

    setup_app_logger(
        app=app,
        filepath=logs_filepath,
    )
    register_routers(app)
    setup_dishka(container, app)

    app.state.register_admin = enable_admin

    return app


def create_default_app() -> FastAPI:
    container = make_async_container(
        resources_provider,
        users_provider,
        DBConnectionProvider(
            logger=get_app_logger('db'),
            database_url=settings.database.url,
        ),
        FastapiProvider(),
    )
    app = create_app(
        container=container,
        logs_filepath=settings.log.path if not settings.server.is_dev else None,
        enable_admin=True,
    )

    register_middlewares(app)

    return app
