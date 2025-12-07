from functools import lru_cache
from typing import Literal

from dotenv import find_dotenv
from pydantic import Secret
from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    env: Literal['dev', 'lab', 'prod'] = 'dev'
    port: int = 8000
    debug: bool = False
    database_url: Secret[str] = Secret('sqlite+aiosqlite:///./test.db')
    max_records_per_page: int = 100
    logs_path: str = './.logs/app.log'

    @property
    def is_dev(self) -> bool:
        return self.env == 'dev'

    @property
    def is_lab(self) -> bool:
        return self.env == 'lab'

    @property
    def is_prod(self) -> bool:
        return self.env == 'prod'

    @property
    def scheme(self) -> Literal['http', 'https']:
        return 'http' if self.is_dev else 'https'

    @property
    def use_log_rotation(self) -> bool:
        return self.env != 'dev' and bool(self.logs_path)

    @property
    def swagger_url(self) -> str:
        return f'{self.scheme}://localhost:{self.port}/docs'

    @property
    def redoc_url(self) -> str:
        return f'{self.scheme}://localhost:{self.port}/redoc'

    class Config:
        env_file = find_dotenv()
        env_file_encoding = 'utf-8'
        case_sensitive = False


@lru_cache
def get_settings() -> _Settings:
    return _Settings()


settings = get_settings()
