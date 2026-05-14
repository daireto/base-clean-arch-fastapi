from pydantic import Secret
from sqlactive import DBConnection
from structlog.stdlib import BoundLogger

from modules.resources.infrastructure.persistence.models.sqlite import (
    BaseModel as SQLiteResourcesBaseModel,
)

base_models = [
    SQLiteResourcesBaseModel,
]


async def init_db(
    logger: BoundLogger, database_url: Secret[str]
) -> DBConnection:
    logger.info('Initializing database')
    conn = DBConnection(database_url.get_secret_value(), echo=False)

    logger.info('Initializing tables')
    await conn.init_db(*base_models)

    logger.info('Database and tables initialized')
    return conn
