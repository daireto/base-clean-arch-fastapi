from uuid import UUID

from pydantic import BaseModel
from simple_result import Err, Ok, Result

from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from shared.application.instrumentation import DeletionUseCaseInstrumentation
from shared.application.interfaces.command_handler import CommandHandler


class DeleteUserCommand(BaseModel):
    id: UUID


class DeleteUserHandler(CommandHandler):
    def __init__(
        self,
        user_repository: UserRepositoryABC,
        instrumentation: DeletionUseCaseInstrumentation | None = None,
    ) -> None:
        self._user_repository = user_repository
        self._instrumentation = instrumentation or DeletionUseCaseInstrumentation()

    async def handle(self, command: DeleteUserCommand) -> Result[None, Exception]:
        self._instrumentation.before(command.id)

        try:
            await self._user_repository.delete(command.id)
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(command.id)
        return Ok(None)
