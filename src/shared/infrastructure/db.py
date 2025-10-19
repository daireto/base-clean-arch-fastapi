from sqlactive import ActiveRecordBaseModel, DBConnection

from src.core.config import settings
from src.core.logger import async_log_decorator, get_logger

logger = get_logger('db')


@async_log_decorator(
    logger=logger,
    on_start_msg='Initializing database',
    on_end_msg='Database initialized',
    on_error_msg='Error initializing database',
)
async def init_db(base_models: list[type[ActiveRecordBaseModel]]) -> DBConnection:
    conn = DBConnection(settings.database_url.get_secret_value(), echo=False)
    for model in base_models:
        await conn.init_db(model)
    return conn
