from uuid import UUID

from structlog.stdlib import BoundLogger

from src.core.logger import get_app_logger
from src.shared.application.interfaces.base import Instrumentation


class DeleteResourceInstrumentation(Instrumentation):
    def __init__(self, logger: BoundLogger | None = None) -> None:
        self._logger = logger or get_app_logger('resources.delete')

    def before(self, id_: UUID) -> None:
        self._logger.info(
            'Deleting resource',
            resource_id=id_,
        )

    def after(self, id_: UUID) -> None:
        self._logger.info(
            'Resource deleted',
            resource_id=id_,
        )

    def error(self, error: Exception) -> None:
        self._logger.exception(
            'Error deleting resource',
            exc_info=error,
        )

    def not_found(self, id_: UUID) -> None:
        self._logger.info(
            'Resource not found',
            resource_id=id_,
        )
