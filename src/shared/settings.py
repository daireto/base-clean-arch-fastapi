from starlette.config import Config

config = Config()

DATABASE_URL = config(
    'DATABASE_URL',
    cast=str,
    default='sqlite+aiosqlite:///:memory:',
)
MAX_RECORDS_PER_PAGE = config('MAX_RECORDS_PER_PAGE', cast=int, default=100)
