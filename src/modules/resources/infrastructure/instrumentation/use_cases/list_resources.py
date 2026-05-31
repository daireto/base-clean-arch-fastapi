from modules.resources.domain.entities import Resource
from shared.application.interfaces.instrumentation import UseCaseInstrumentation


class ListResourcesInstrumentation(UseCaseInstrumentation):
    def before(self) -> None:
        super().before('Listing resources')

    def after(self, resources: list[Resource]) -> None:
        super().after('Resources listed', resources_count=len(resources))

    def error(self, error: Exception) -> None:
        super().error('Error listing resources', error)
