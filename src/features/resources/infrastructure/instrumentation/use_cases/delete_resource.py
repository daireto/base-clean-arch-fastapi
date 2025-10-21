from uuid import UUID

from src.core.logger import get_app_logger
from src.shared.application.interfaces.instrumentation import Instrumentation


class DeleteResourceInstrumentation(Instrumentation):
    def __init__(self) -> None:
        super().__init__(logger=get_app_logger('resources.delete'))

    def before(self, id_: UUID) -> None:
        super().before('Deleting resource', resource_id=id_)

    def after(self, id_: UUID) -> None:
        super().after('Resource deleted', resource_id=id_)

    def error(self, error: Exception) -> None:
        super().error('Error deleting resource', error)

    def not_found(self, id_: UUID) -> None:
        super().not_found('Resource not found', resource_id=id_)
