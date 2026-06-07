from uuid import UUID

from modules.resources.domain.entities import Resource
from shared.application.instrumentation import (
    CreationUseCaseInstrumentation,
    DeletionUseCaseInstrumentation,
    ListingUseCaseInstrumentation,
    RetrievalUseCaseInstrumentation,
    UpdateUseCaseInstrumentation,
)


class CreateResourceInstrumentation(CreationUseCaseInstrumentation[Resource]):
    def before(self, resource: Resource) -> None:
        self._logger.info('Creating resource', resource_id=resource.id)

    def after(self, resource: Resource) -> None:
        self._logger.info('Resource created', resource_id=resource.id)

    def error(self, error: Exception) -> None:
        self._logger.exception('Error creating resource', exc_info=error)


class DeleteResourceInstrumentation(DeletionUseCaseInstrumentation):
    def before(self, id_: UUID) -> None:
        self._logger.info('Deleting resource', resource_id=id_)

    def after(self, id_: UUID) -> None:
        self._logger.info('Resource deleted', resource_id=id_)

    def error(self, error: Exception) -> None:
        self._logger.exception('Error deleting resource', exc_info=error)


class GetResourceInstrumentation(RetrievalUseCaseInstrumentation[Resource]):
    def before(self, id_: UUID) -> None:
        self._logger.info('Getting resource', resource_id=id_)

    def after(self, resource: Resource) -> None:
        self._logger.info('Resource got', resource_id=resource.id)

    def error(self, error: Exception) -> None:
        self._logger.exception('Error getting resource', exc_info=error)

    def not_found(self, id_: UUID) -> None:
        self._logger.warning('Resource not found', resource_id=id_)


class ListResourcesInstrumentation(ListingUseCaseInstrumentation[Resource]):
    def before(self) -> None:
        self._logger.info('Listing resources')

    def after(self, resources: list[Resource]) -> None:
        self._logger.info('Resources listed', resources_count=len(resources))

    def error(self, error: Exception) -> None:
        self._logger.exception('Error listing resources', exc_info=error)


class UpdateResourceInstrumentation(UpdateUseCaseInstrumentation[Resource]):
    def before(self, resource: Resource) -> None:
        self._logger.info('Updating resource', resource_id=resource.id)

    def after(self, resource: Resource, created: bool = False) -> None:
        if created:
            self._logger.info(
                'Resource created as it did not exist',
                resource_id=resource.id,
            )
        else:
            self._logger.info('Resource updated', resource_id=resource.id)

    def error(self, error: Exception) -> None:
        self._logger.exception('Error updating resource', exc_info=error)

    def not_found(self, id_: UUID) -> None:
        self._logger.warning('Resource not found', resource_id=id_)
