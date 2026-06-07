from dishka import Provider, Scope

from core.logger import get_app_logger
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from modules.users.infrastructure.instrumentation.use_cases import (
    CreateUserInstrumentation,
    DeleteUserInstrumentation,
    GetUserInstrumentation,
    ListUsersInstrumentation,
    UpdateUserInstrumentation,
)
from modules.users.infrastructure.persistence.repositories.sqlite import (
    SQLiteUserRepository,
)
from shared.application.instrumentation import (
    CreationUseCaseInstrumentation,
    DeletionUseCaseInstrumentation,
    ListingUseCaseInstrumentation,
    RetrievalUseCaseInstrumentation,
    UpdateUseCaseInstrumentation,
)


def get_create_user_instrumentation() -> CreateUserInstrumentation:
    return CreateUserInstrumentation(logger=get_app_logger('users.create'))


def get_delete_user_instrumentation() -> DeleteUserInstrumentation:
    return DeleteUserInstrumentation(logger=get_app_logger('users.delete'))


def get_retrieve_user_instrumentation() -> GetUserInstrumentation:
    return GetUserInstrumentation(logger=get_app_logger('users.retrieve'))


def get_list_users_instrumentation() -> ListUsersInstrumentation:
    return ListUsersInstrumentation(logger=get_app_logger('users.list'))


def get_update_user_instrumentation() -> UpdateUserInstrumentation:
    return UpdateUserInstrumentation(logger=get_app_logger('users.update'))


provider = Provider(scope=Scope.APP)
provider.provide(SQLiteUserRepository, provides=UserRepositoryABC)
provider.provide(
    get_create_user_instrumentation,
    provides=CreationUseCaseInstrumentation,
)
provider.provide(
    get_delete_user_instrumentation,
    provides=DeletionUseCaseInstrumentation,
)
provider.provide(
    get_retrieve_user_instrumentation,
    provides=RetrievalUseCaseInstrumentation,
)
provider.provide(
    get_list_users_instrumentation,
    provides=ListingUseCaseInstrumentation,
)
provider.provide(
    get_update_user_instrumentation,
    provides=UpdateUseCaseInstrumentation,
)
