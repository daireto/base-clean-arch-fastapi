from pydantic import BaseModel, EmailStr, SecretStr
from simple_result import Err, Ok, Result

from modules.users.domain.entities import User
from modules.users.domain.enums import Gender
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from shared.application.instrumentation import CreationUseCaseInstrumentation
from shared.application.interfaces.command_handler import CommandHandler


class CreateUserCommand(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    gender: Gender | str
    password: SecretStr


class CreateUserHandler(CommandHandler):
    def __init__(
        self,
        user_repository: UserRepositoryABC,
        instrumentation: CreationUseCaseInstrumentation[User] | None = None,
    ) -> None:
        self._user_repository = user_repository
        self._instrumentation = instrumentation or CreationUseCaseInstrumentation()

    async def handle(
        self,
        command: CreateUserCommand,
    ) -> Result[User, Exception]:
        user = User(
            username=command.username,
            fullname=command.fullname,
            email=command.email,
            gender=command.gender,  # type: ignore
        )
        self._instrumentation.before(user)

        try:
            created = await self._user_repository.create(user, command.password)
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(created)
        return Ok(created)
