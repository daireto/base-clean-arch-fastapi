from logger import get_app_logger
from modules.resources.domain.entities import Resource
from shared.application.interfaces.instrumentation import Instrumentation


class ListResourcesInstrumentation(Instrumentation):
    def __init__(self) -> None:
        super().__init__(logger=get_app_logger('resources.list'))

    def before(self) -> None:
        super().before('Listing resources')

    def after(self, resources: list[Resource]) -> None:
        super().after('Resources listed', resources_count=len(resources))

    def error(self, error: Exception) -> None:
        super().error('Error listing resources', error)
