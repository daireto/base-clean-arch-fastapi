from starlette.config import Config

config = Config('.env')


class SharedSettings:
    DATABASE_URL = config(
        'DATABASE_URL',
        cast=str,
        default='aiosqlite:///database.db',
    )
