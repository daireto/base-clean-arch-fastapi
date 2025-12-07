from abc import ABC
from typing import Any

from pydantic import BaseModel

from shared.domain.error_codes import ErrorCodes


class ErrorDetail(BaseModel):
    code: str
    message: str
    extra: dict[str, Any] | None = None


class DomainError(Exception, ABC):
    def __init__(self, status_code: int, detail: ErrorDetail) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail.message)


# Generic errors
class AuthenticationError(DomainError):
    def __init__(self, detail: ErrorDetail | None = None) -> None:
        super().__init__(
            status_code=401,
            detail=detail
            or ErrorDetail(
                code=ErrorCodes.AUTHENTICATION_ERROR,
                message='Authentication error',
            ),
        )


class AuthorizationError(DomainError):
    def __init__(self, detail: ErrorDetail | None = None) -> None:
        super().__init__(
            status_code=403,
            detail=detail
            or ErrorDetail(
                code=ErrorCodes.AUTHORIZATION_ERROR,
                message='Authorization error',
            ),
        )


class InvalidInputError(DomainError):
    def __init__(self, detail: ErrorDetail) -> None:
        super().__init__(
            status_code=400,
            detail=detail,
        )


class NotFoundError(DomainError):
    def __init__(self, detail: ErrorDetail) -> None:
        super().__init__(
            status_code=404,
            detail=detail,
        )


# Specific errors
class InvalidURLError(InvalidInputError):
    def __init__(self, url: str) -> None:
        super().__init__(
            ErrorDetail(
                code=ErrorCodes.INVALID_URL,
                message='URL is not valid',
                extra={'url': url},
            ),
        )
