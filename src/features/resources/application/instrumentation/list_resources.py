from structlog.stdlib import BoundLogger

from src.core.logger import get_app_logger
from src.features.resources.domain.entities import Resource
from src.shared.application.interfaces.base import Instrumentation


class ListResourcesInstrumentation(Instrumentation):
    def __init__(self, logger: BoundLogger | None = None) -> None:
        self._logger = logger or get_app_logger('resources.list')

    def before(self) -> None:
        self._logger.info('Listing resources')

    def after(self, resources: list[Resource]) -> None:
        self._logger.info(
            'Resources listed',
            resources_count=len(resources),
        )

    def error(self, error: Exception) -> None:
        self._logger.exception(
            'Error listing resources',
            exc_info=error,
        )
