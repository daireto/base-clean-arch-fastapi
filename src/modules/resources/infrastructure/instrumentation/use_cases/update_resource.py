from uuid import UUID

from modules.resources.domain.entities import Resource
from shared.application.interfaces.instrumentation import UseCaseInstrumentation


class UpdateResourceInstrumentation(UseCaseInstrumentation):
    def before(self, resource: Resource) -> None:
        super().before('Updating resource', resource_id=resource.id)

    def after(self, resource: Resource, created: bool = False) -> None:
        if created:
            super().after(
                'Resource created as it did not exist',
                resource_id=resource.id,
            )
        else:
            super().after('Resource updated', resource_id=resource.id)

    def error(self, error: Exception) -> None:
        super().error('Error updating resource', error)

    def not_found(self, id_: UUID) -> None:
        super().not_found('Resource not found', resource_id=id_)
