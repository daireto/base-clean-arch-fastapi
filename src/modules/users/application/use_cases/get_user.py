from uuid import UUID

from pydantic import BaseModel
from simple_result import Err, Ok, Result

from modules.users.domain.entities import User
from modules.users.domain.exceptions import UserNotFoundError
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from shared.application.instrumentation import RetrievalUseCaseInstrumentation
from shared.application.interfaces.command_handler import CommandHandler


class GetUserCommand(BaseModel):
    id: UUID


class GetUserHandler(CommandHandler):
    def __init__(
        self,
        user_repository: UserRepositoryABC,
        instrumentation: RetrievalUseCaseInstrumentation[User] | None = None,
    ) -> None:
        self._user_repository = user_repository
        self._instrumentation = instrumentation or RetrievalUseCaseInstrumentation()

    async def handle(self, command: GetUserCommand) -> Result[User, Exception]:
        self._instrumentation.before(command.id)

        try:
            user = await self._user_repository.get_by_id(command.id)
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        if not user:
            self._instrumentation.not_found(command.id)
            return Err(UserNotFoundError(command.id))

        self._instrumentation.after(user)
        return Ok(user)
