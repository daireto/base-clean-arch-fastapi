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
        self.__logger.info('Initializing database connection')
        conn = await init_db(database_url=self.__database_url)
        self.__logger.info('Database connection initialized')
        yield conn
        self.__logger.info('Closing database connection')
        await conn.close()
        self.__logger.info('Database connection closed')
