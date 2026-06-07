from enum import StrEnum


class ErrorCode(StrEnum):
    MISSING_PASSWORD = 'MISSING_PASSWORD'  # noqa: S105
    USER_NOT_FOUND = 'USER_NOT_FOUND'
