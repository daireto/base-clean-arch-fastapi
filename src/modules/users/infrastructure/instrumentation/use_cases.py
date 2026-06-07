from uuid import UUID

from modules.users.domain.entities import User
from shared.application.instrumentation import (
    CreationUseCaseInstrumentation,
    DeletionUseCaseInstrumentation,
    ListingUseCaseInstrumentation,
    RetrievalUseCaseInstrumentation,
    UpdateUseCaseInstrumentation,
)


class CreateUserInstrumentation(CreationUseCaseInstrumentation[User]):
    def before(self, user: User) -> None:
        self._logger.info('Creating user', user_id=user.id)

    def after(self, user: User) -> None:
        self._logger.info('User created', user_id=user.id)

    def error(self, error: Exception) -> None:
        self._logger.exception('Error creating user', exc_info=error)


class DeleteUserInstrumentation(DeletionUseCaseInstrumentation):
    def before(self, id_: UUID) -> None:
        self._logger.info('Deleting user', user_id=id_)

    def after(self, id_: UUID) -> None:
        self._logger.info('User deleted', user_id=id_)

    def error(self, error: Exception) -> None:
        self._logger.exception('Error deleting user', exc_info=error)


class GetUserInstrumentation(RetrievalUseCaseInstrumentation[User]):
    def before(self, id_: UUID) -> None:
        self._logger.info('Getting user', user_id=id_)

    def after(self, user: User) -> None:
        self._logger.info('User got', user_id=user.id)

    def error(self, error: Exception) -> None:
        self._logger.exception('Error getting user', exc_info=error)

    def not_found(self, id_: UUID) -> None:
        self._logger.warning('User not found', user_id=id_)


class ListUsersInstrumentation(ListingUseCaseInstrumentation[User]):
    def before(self) -> None:
        self._logger.info('Listing users')

    def after(self, users: list[User]) -> None:
        self._logger.info('Users listed', users_count=len(users))

    def error(self, error: Exception) -> None:
        self._logger.exception('Error listing users', exc_info=error)


class UpdateUserInstrumentation(UpdateUseCaseInstrumentation[User]):
    def before(self, user: User) -> None:
        self._logger.info('Updating user', user_id=user.id)

    def after(self, user: User, created: bool = False) -> None:
        if created:
            self._logger.info(
                'User created as it did not exist',
                user_id=user.id,
            )
        else:
            self._logger.info('User updated', user_id=user.id)

    def error(self, error: Exception) -> None:
        self._logger.exception('Error updating user', exc_info=error)

    def not_found(self, id_: UUID) -> None:
        self._logger.warning('User not found', user_id=id_)
