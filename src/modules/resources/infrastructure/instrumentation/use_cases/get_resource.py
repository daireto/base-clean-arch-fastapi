from uuid import UUID

from modules.resources.domain.entities import Resource
from shared.application.interfaces.instrumentation import UseCaseInstrumentation


class GetResourceInstrumentation(UseCaseInstrumentation):
    def before(self, id_: UUID) -> None:
        super().before('Getting resource', resource_id=id_)

    def after(self, resource: Resource) -> None:
        super().after('Resource got', resource_id=resource.id)

    def error(self, error: Exception) -> None:
        super().error('Error getting resource', error)

    def not_found(self, id_: UUID) -> None:
        super().not_found('Resource not found', resource_id=id_)
