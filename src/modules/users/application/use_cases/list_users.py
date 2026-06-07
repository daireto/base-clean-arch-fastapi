from pydantic import BaseModel, ConfigDict
from simple_result import Err, Ok, Result

from modules.users.domain.collections import UserCollection
from modules.users.domain.entities import User
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from shared.application.instrumentation import ListingUseCaseInstrumentation
from shared.application.interfaces.command_handler import CommandHandler
from shared.helpers.odata_helper import ODataHelper


class ListUsersCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    odata: ODataHelper


class ListUsersHandler(CommandHandler):
    def __init__(
        self,
        user_repository: UserRepositoryABC,
        instrumentation: ListingUseCaseInstrumentation[User] | None = None,
    ) -> None:
        self._user_repository = user_repository
        self._instrumentation = instrumentation or ListingUseCaseInstrumentation()

    async def handle(
        self,
        command: ListUsersCommand,
    ) -> Result[UserCollection, Exception]:
        self._instrumentation.before()

        try:
            users = await self._user_repository.all(command.odata.get())
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(users)
        return Ok(UserCollection(users))

    async def handle_with_count(
        self,
        command: ListUsersCommand,
    ) -> Result[UserCollection, Exception]:
        self._instrumentation.before()

        try:
            users = await self._user_repository.all(command.odata.get())
            total = await self._user_repository.count(command.odata.get_for_counting())
        except Exception as error:
            self._instrumentation.error(error)
            return Err(error)

        self._instrumentation.after(users)
        return Ok(UserCollection(users, total))
