from uuid import UUID

from shared.application.interfaces.instrumentation import UseCaseInstrumentation


class DeleteResourceInstrumentation(UseCaseInstrumentation):
    def before(self, id_: UUID) -> None:
        super().before('Deleting resource', resource_id=id_)

    def after(self, id_: UUID) -> None:
        super().after('Resource deleted', resource_id=id_)

    def error(self, error: Exception) -> None:
        super().error('Error deleting resource', error)
