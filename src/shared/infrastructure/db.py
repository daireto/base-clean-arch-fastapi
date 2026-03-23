from sqlactive import DBConnection

from app.config import settings
from app.logger import get_logger
from modules.resources.infrastructure.persistence.models.sqlite import (
    BaseModel as SQLiteResourcesBaseModel,
)

logger = get_logger('db')

base_models = [
    SQLiteResourcesBaseModel,
]


async def init_db() -> DBConnection:
    logger.info('Initializing database')
    conn = DBConnection(settings.database_url.get_secret_value(), echo=False)

    logger.info('Initializing tables')
    await conn.init_db(*base_models)

    logger.info('Database and tables initialized')
    return conn
