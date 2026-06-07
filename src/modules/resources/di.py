from dishka import Provider, Scope

from core.logger import get_app_logger
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from modules.resources.infrastructure.instrumentation.use_cases import (
    CreateResourceInstrumentation,
    DeleteResourceInstrumentation,
    GetResourceInstrumentation,
    ListResourcesInstrumentation,
    UpdateResourceInstrumentation,
)
from modules.resources.infrastructure.persistence.repositories.sqlite import (
    SQLiteResourceRepository,
)
from shared.application.instrumentation import (
    CreationUseCaseInstrumentation,
    DeletionUseCaseInstrumentation,
    ListingUseCaseInstrumentation,
    RetrievalUseCaseInstrumentation,
    UpdateUseCaseInstrumentation,
)


def get_create_resource_instrumentation() -> CreateResourceInstrumentation:
    return CreateResourceInstrumentation(logger=get_app_logger('resources.create'))


def get_delete_resource_instrumentation() -> DeleteResourceInstrumentation:
    return DeleteResourceInstrumentation(logger=get_app_logger('resources.delete'))


def get_retrieve_resource_instrumentation() -> GetResourceInstrumentation:
    return GetResourceInstrumentation(logger=get_app_logger('resources.retrieve'))


def get_list_resources_instrumentation() -> ListResourcesInstrumentation:
    return ListResourcesInstrumentation(logger=get_app_logger('resources.list'))


def get_update_resource_instrumentation() -> UpdateResourceInstrumentation:
    return UpdateResourceInstrumentation(logger=get_app_logger('resources.update'))


provider = Provider(scope=Scope.APP)
provider.provide(SQLiteResourceRepository, provides=ResourceRepositoryABC)
provider.provide(
    get_create_resource_instrumentation,
    provides=CreationUseCaseInstrumentation,
)
provider.provide(
    get_delete_resource_instrumentation,
    provides=DeletionUseCaseInstrumentation,
)
provider.provide(
    get_retrieve_resource_instrumentation,
    provides=RetrievalUseCaseInstrumentation,
)
provider.provide(
    get_list_resources_instrumentation,
    provides=ListingUseCaseInstrumentation,
)
provider.provide(
    get_update_resource_instrumentation,
    provides=UpdateUseCaseInstrumentation,
)
