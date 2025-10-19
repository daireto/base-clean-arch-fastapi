from uuid import UUID

from structlog.stdlib import BoundLogger

from src.core.logger import get_app_logger
from src.features.resources.domain.entities import Resource
from src.shared.application.interfaces.base import Instrumentation


class GetResourceInstrumentation(Instrumentation):
    def __init__(self, logger: BoundLogger | None = None) -> None:
        self._logger = logger or get_app_logger('resources.get')

    def before(self, id_: UUID) -> None:
        self._logger.info(
            'Getting resource',
            resource_id=id_,
        )

    def after(self, resource: Resource) -> None:
        self._logger.info(
            'Resource retrieved',
            resource_id=resource.id,
        )

    def error(self, error: Exception) -> None:
        self._logger.exception(
            'Error getting resource',
            exc_info=error,
        )

    def not_found(self, id_: UUID) -> None:
        self._logger.info(
            'Resource not found',
            resource_id=id_,
        )
