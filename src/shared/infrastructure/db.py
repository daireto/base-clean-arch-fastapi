from sqlactive import ActiveRecordBaseModel, DBConnection

from api.config import settings
from logger import async_log_decorator, get_logger

logger = get_logger('db')

conn = DBConnection(settings.database_url.get_secret_value(), echo=False)


@async_log_decorator(
    logger=logger,
    on_start_msg='Initializing database',
    on_end_msg='Database initialized',
    on_error_msg='Error initializing database',
)
async def init_db(base_models: list[type[ActiveRecordBaseModel]]) -> None:
    for model in base_models:
        await conn.init_db(model)
