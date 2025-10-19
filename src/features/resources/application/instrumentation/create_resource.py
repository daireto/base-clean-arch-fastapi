from structlog.stdlib import BoundLogger

from src.core.logger import get_app_logger
from src.features.resources.domain.entities import Resource
from src.shared.application.interfaces.base import Instrumentation


class CreateResourceInstrumentation(Instrumentation):
    def __init__(self, logger: BoundLogger | None = None) -> None:
        self._logger = logger or get_app_logger('resources.create')

    def before(self, resource: Resource) -> None:
        self._logger.info(
            'Creating resource',
            resource_id=resource.id,
        )

    def after(self, resource: Resource) -> None:
        self._logger.info(
            'Resource created',
            resource_id=resource.id,
        )

    def error(self, error: Exception) -> None:
        self._logger.exception(
            'Error creating resource',
            exc_info=error,
        )
