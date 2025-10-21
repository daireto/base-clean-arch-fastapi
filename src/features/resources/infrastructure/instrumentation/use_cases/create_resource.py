from src.core.logger import get_app_logger
from src.features.resources.domain.entities import Resource
from src.shared.application.interfaces.instrumentation import Instrumentation


class CreateResourceInstrumentation(Instrumentation):
    def __init__(self) -> None:
        super().__init__(logger=get_app_logger('resources.create'))

    def before(self, resource: Resource) -> None:
        super().before('Creating resource', resource_id=resource.id)

    def after(self, resource: Resource) -> None:
        super().after('Resource created', resource_id=resource.id)

    def error(self, error: Exception) -> None:
        super().error('Error creating resource', error)
