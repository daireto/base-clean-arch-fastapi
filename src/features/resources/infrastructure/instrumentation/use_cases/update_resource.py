from src.core.logger import get_app_logger
from src.features.resources.domain.entities import Resource
from src.shared.application.interfaces.instrumentation import Instrumentation


class UpdateResourceInstrumentation(Instrumentation):
    def __init__(self) -> None:
        super().__init__(logger=get_app_logger('resources.update'))

    def before(self, resource: Resource) -> None:
        super().before('Updating resource', resource_id=resource.id)

    def after(self, resource: Resource) -> None:
        super().after('Resource updated', resource_id=resource.id)

    def error(self, error: Exception) -> None:
        super().error('Error updating resource', error)

    def not_found(self, resource: Resource) -> None:
        super().not_found('Resource not found', resource_id=resource.id)
