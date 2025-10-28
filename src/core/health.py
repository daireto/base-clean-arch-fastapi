from enum import Enum
from functools import lru_cache

from pydantic import BaseModel


class HealthStatus(str, Enum):
    HEALTHY = 'healthy'
    UNHEALTHY = 'unhealthy'


class ServerHealthResponse(BaseModel):
    message: str
    status: HealthStatus


class _ServerHealth:
    def __init__(self) -> None:
        self.reset()

    @property
    def is_healthy(self) -> bool:
        return self._is_healthy

    @is_healthy.setter
    def is_healthy(self, value: bool) -> None:
        self._is_healthy = value

    def reset(self) -> None:
        self._is_healthy = True
        self._unhealthy_reason = ''

    def set_unhealthy(self, reason: str) -> None:
        self._is_healthy = False
        self._unhealthy_reason = reason

    def get_unhealthy_reason(self) -> str:
        return self._unhealthy_reason

    def to_response(self) -> ServerHealthResponse:
        return ServerHealthResponse(
            message='ok' if self.is_healthy else self.get_unhealthy_reason(),
            status=HealthStatus.HEALTHY
            if self.is_healthy
            else HealthStatus.UNHEALTHY,
        )

    def __str__(self) -> str:
        return (
            HealthStatus.HEALTHY
            if self.is_healthy
            else f'{HealthStatus.UNHEALTHY}: {self.get_unhealthy_reason()}'
        )

    def __bool__(self) -> bool:
        return self.is_healthy


@lru_cache
def get_server_health() -> _ServerHealth:
    return _ServerHealth()


server_health = get_server_health()
