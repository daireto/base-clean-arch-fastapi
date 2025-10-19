from abc import ABC, abstractmethod
from typing import Any


class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, *args, **kwargs) -> Any:
        pass


class Instrumentation(ABC):
    @abstractmethod
    def before(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def after(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def error(self, error: Exception) -> None:
        pass
