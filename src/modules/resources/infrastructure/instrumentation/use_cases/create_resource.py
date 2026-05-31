from modules.resources.domain.entities import Resource
from shared.application.interfaces.instrumentation import UseCaseInstrumentation


class CreateResourceInstrumentation(UseCaseInstrumentation):
    def before(self, resource: Resource) -> None:
        super().before('Creating resource', resource_id=resource.id)

    def after(self, resource: Resource) -> None:
        super().after('Resource created', resource_id=resource.id)

    def error(self, error: Exception) -> None:
        super().error('Error creating resource', error)
