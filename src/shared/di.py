from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from pydantic import Secret
from sqlactive import DBConnection
from structlog.stdlib import BoundLogger

from shared.infrastructure.db import init_db


class DBConnectionProvider(Provider):
    def __init__(self, logger: BoundLogger, database_url: Secret[str]) -> None:
        super().__init__()
        self.__logger = logger
        self.__database_url = database_url

    @provide(scope=Scope.APP)
    async def get_db_connection(self) -> AsyncIterable[DBConnection]:
        conn = await init_db(
            logger=self.__logger,
            database_url=self.__database_url,
        )
        yield conn
        await conn.close()
