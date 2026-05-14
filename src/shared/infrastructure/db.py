from pydantic import Secret
from sqlactive import DBConnection

from modules.resources.infrastructure.persistence.models.sqlite import (
    BaseModel as SQLiteResourcesBaseModel,
)

base_models = [
    SQLiteResourcesBaseModel,
]


async def init_db(database_url: Secret[str]) -> DBConnection:
    conn = DBConnection(database_url.get_secret_value(), echo=False)
    await conn.init_db(*base_models)
    return conn
