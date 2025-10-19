from abc import ABC

from src.shared.domain.error_codes import ErrorCodes


class DomainError(Exception, ABC):
    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        **kwargs,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.input_info = kwargs
        super().__init__(message)


class AuthenticationError(DomainError):
    pass


class AuthorizationError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class InvalidInputError(DomainError):
    pass


class NotFoundError(DomainError):
    pass


class InvalidURLError(InvalidInputError):
    def __init__(self, url: str) -> None:
        super().__init__(
            message='URL is not valid',
            error_code=ErrorCodes.INVALID_URL,
            url=url,
        )
