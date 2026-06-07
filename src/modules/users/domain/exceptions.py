from uuid import UUID

from modules.users.domain.error_codes import ErrorCode
from shared.domain.bases.error import Error


class MissingPasswordError(Error):
    def __init__(self, id_: UUID) -> None:
        self.id = id_
        super().__init__(
            status=422,
            title='Missing Password',
            detail='Password is required to create a new user.',
            code=ErrorCode.MISSING_PASSWORD,
            extra={'user_id': id_},
        )


class UserNotFoundError(Error):
    def __init__(self, id_: UUID) -> None:
        self.id = id_
        super().__init__(
            status=404,
            title='User Not Found',
            detail='The user was not found.',
            code=ErrorCode.USER_NOT_FOUND,
            extra={'user_id': id_},
        )
