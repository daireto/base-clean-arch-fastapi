from structlog.stdlib import BoundLogger

from src.core.logger import get_app_logger
from src.features.resources.domain.entities import Resource
from src.shared.application.interfaces.base import Instrumentation


class UpdateResourceInstrumentation(Instrumentation):
    def __init__(self, logger: BoundLogger | None = None) -> None:
        self._logger = logger or get_app_logger('resources.update')

    def before(self, resource: Resource) -> None:
        self._logger.info(
            'Updating resource',
            resource_id=resource.id,
        )

    def after(self, resource: Resource) -> None:
        self._logger.info(
            'Resource updated',
            resource_id=resource.id,
        )

    def error(self, error: Exception) -> None:
        self._logger.exception(
            'Error updating resource',
            exc_info=error,
        )

    def not_found(self, resource: Resource) -> None:
        self._logger.info(
            'Resource not found for update',
            resource_id=resource.id,
        )
