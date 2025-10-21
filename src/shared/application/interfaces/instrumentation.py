from abc import ABC, abstractmethod

from structlog.stdlib import BoundLogger


class Instrumentation(ABC):
    def __init__(self, logger: BoundLogger) -> None:
        self._logger = logger

    @abstractmethod
    def before(self, message: str, **kwargs) -> None:
        self._logger.info(message, **kwargs)

    @abstractmethod
    def after(self, message: str, **kwargs) -> None:
        self._logger.info(message, **kwargs)

    @abstractmethod
    def error(self, message: str, error: Exception, **kwargs) -> None:
        self._logger.exception(message, **kwargs, exc_info=error)

    def not_found(self, message: str, **kwargs) -> None:
        self._logger.warning(message, **kwargs)
