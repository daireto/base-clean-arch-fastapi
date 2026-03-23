from shared.domain.bases.error import Error
from shared.domain.error_codes import ErrorCode


class AuthenticationError(Error):
    def __init__(
        self,
        detail: str | None = None,
        **extra,
    ) -> None:
        super().__init__(
            status=401,
            title='Authentication Error',
            detail=detail or 'User is not authenticated.',
            code=ErrorCode.AUTHENTICATION_ERROR,
            extra=extra,
        )


class AuthorizationError(Error):
    def __init__(
        self,
        detail: str | None = None,
        **extra,
    ) -> None:
        super().__init__(
            status=403,
            title='Insufficient Permissions',
            detail=detail or 'User has not enough permissions.',
            code=ErrorCode.AUTHORIZATION_ERROR,
            extra=extra,
        )
