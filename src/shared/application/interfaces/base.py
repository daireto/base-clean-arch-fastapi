from abc import ABC, abstractmethod
from typing import Any


class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, *args, **kwargs) -> Any:
        pass
