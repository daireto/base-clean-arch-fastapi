from uuid import UUID

from src.core.logger import get_app_logger
from src.features.resources.domain.entities import Resource
from src.shared.application.interfaces.instrumentation import Instrumentation


class GetResourceInstrumentation(Instrumentation):
    def __init__(self) -> None:
        super().__init__(logger=get_app_logger('resources.get'))

    def before(self, id_: UUID) -> None:
        super().before('Getting resource', resource_id=id_)

    def after(self, resource: Resource) -> None:
        super().after('Resource got', resource_id=resource.id)

    def error(self, error: Exception) -> None:
        super().error('Error getting resource', error)

    def not_found(self, id_: UUID) -> None:
        super().not_found('Resource not found', resource_id=id_)
