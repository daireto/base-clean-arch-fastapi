from modules.resources.domain.entities import Resource
from shared.application.instrumentation import Instrumentation


class UpdateResourceInstrumentation(Instrumentation):
    def before(self, resource: Resource) -> None:
        super().before('Updating resource', resource_id=resource.id)

    def after(self, resource: Resource) -> None:
        super().after('Resource updated', resource_id=resource.id)

    def error(self, error: Exception) -> None:
        super().error('Error updating resource', error)
