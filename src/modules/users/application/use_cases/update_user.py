from uuid import UUID

from pydantic import BaseModel, EmailStr
from simple_result import Err, Ok, Result

from modules.users.domain.entities import User
from modules.users.domain.enums import Gender, Role
from modules.users.domain.exceptions import MissingPasswordError, UserNotFoundError
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from shared.application.instrumentation import UpdateUseCaseInstrumentation
from shared.application.interfaces.command_handler import CommandHandler
from shared.utils.validation_types import HashedSecretStr


class UpdateUserCommand(BaseModel):
    id: UUID
    username: str
    fullname: str
    email: EmailStr
    gender: Gender | str
    role: Role | str
    password: HashedSecretStr | None = None


class PartialUpdateUserCommand(BaseModel):
    id: UUID
    username: str | None = None
    fullname: str | None = None
    email: EmailStr | None = None
    gender: Gender | str | None = None
    role: Role | str | None = None
    password: HashedSecretStr | None = None


class UpdateUserHandler(CommandHandler):
    def __init__(
        self,
        user_repository: UserRepositoryABC,
        instrumentation: UpdateUseCaseInstrumentation[User] | None = None,
    ) -> None:
        self._user_repository = user_repository
        self._instrumentation = instrumentation or UpdateUseCaseInstrumentation()

    async def handle(
        self,
        command: UpdateUserCommand,
    ) -> Result[User, Exception]:
        user = User(
            id=command.id,
            username=command.username,
            fullname=command.fullname,
            email=command.email,
            gender=command.gender,  # type: ignore
            role=command.role,  # type: ignore
        )
        self._instrumentation.before(user)

        try:
            updated = await self._user_repository.update(user, command.password)
            if not updated:
                if not command.password:
                    error = MissingPasswordError(user.id)
                    self._instrumentation.validation_error(error)
                    return Err(error)
                updated = await self._user_repository.create(user, command.password)
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(updated, created=not bool(user))
        return Ok(updated)

    async def handle_partial(
        self,
        command: PartialUpdateUserCommand,
    ) -> Result[User, Exception]:
        user = await self._user_repository.get_by_id(command.id)
        if not user:
            self._instrumentation.not_found(command.id)
            return Err(UserNotFoundError(command.id))

        self._instrumentation.before(user)
        user = user.update(command, exclude_secrets=True)

        try:
            updated = await self._user_repository.update(user, command.password)
            if not updated:
                self._instrumentation.not_found(user.id)
                return Err(UserNotFoundError(user.id))
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(updated)
        return Ok(updated)
