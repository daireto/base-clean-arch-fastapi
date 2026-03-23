from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlactive import DBConnection

from shared.infrastructure.db import init_db


class DBConnectionProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_db_connection(self) -> AsyncIterable[DBConnection]:
        conn = await init_db()
        yield conn
        await conn.close()
