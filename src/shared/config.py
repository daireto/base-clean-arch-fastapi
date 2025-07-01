from starlette.config import Config

config = Config()


class SharedSettings:
    DATABASE_URL = config(
        'DATABASE_URL',
        cast=str,
        default='sqlite+aiosqlite:///database.db',
    )
