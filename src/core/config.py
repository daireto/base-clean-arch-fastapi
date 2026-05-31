from functools import lru_cache
from typing import Literal

from dotenv import find_dotenv
from pydantic import BaseModel, Secret
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseModel):
    env: Literal['dev', 'prod'] = 'dev'
    port: int = 8000
    host: str = 'localhost'
    debug: bool = False
    ssl_certfile: str | None = None
    ssl_keyfile: str | None = None
    allowed_hosts: str = '*'
    behind_proxy: bool = False

    @property
    def is_dev(self) -> bool:
        return self.env == 'dev'

    @property
    def is_prod(self) -> bool:
        return self.env == 'prod'

    @property
    def https(self) -> bool:
        return self.ssl_certfile is not None and self.ssl_keyfile is not None

    @property
    def scheme(self) -> Literal['http', 'https']:
        return 'https' if self.https else 'http'

    @property
    def base_url(self) -> str:
        return f'{self.scheme}://{self.host}:{self.port}'


class CORSConfig(BaseModel):
    allow_origins: str = '*'
    allow_methods: str = '*'
    allow_headers: str = 'X-Requested-With,X-Request-ID'
    expose_headers: str = 'X-Request-ID'


class DatabaseConfig(BaseModel):
    url: Secret[str] = Secret('sqlite+aiosqlite:///./.test.db')


class LogConfig(BaseModel):
    path: str | None = None
    access_log_excluded_path_prefixes: str = 'openapi.json,docs,redoc,health,admin'


class RateLimitConfig(BaseModel):
    storage_uri: Secret[str] = Secret('memory://')
    root_limit: str = '5/second'


class QueryConfig(BaseModel):
    max_records_per_page: int = 100


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_nested_delimiter='__',
        env_nested_max_split=1,
    )

    server: ServerConfig = ServerConfig()
    cors: CORSConfig = CORSConfig()
    database: DatabaseConfig = DatabaseConfig()
    log: LogConfig = LogConfig()
    rate_limit: RateLimitConfig = RateLimitConfig()
    query: QueryConfig = QueryConfig()

    @property
    def swagger_url(self) -> str:
        return f'{self.server.base_url}/docs'

    @property
    def redoc_url(self) -> str:
        return f'{self.server.base_url}/redoc'

    @property
    def admin_url(self) -> str:
        return f'{self.server.base_url}/admin'

    @property
    def startup_msg(self) -> str:
        return (
            f'App started in {self.server.env} mode.'
            f' Listening on port {self.server.port}.'
            f' Docs available at {self.swagger_url} and {self.redoc_url}.'
            f' Admin panel available at {self.admin_url}.'
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
