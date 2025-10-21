from uuid import UUID

EMPTY_UUID = '00000000-0000-0000-0000-000000000000'


class InvalidUUIDError(ValueError):
    def __init__(self, uuid_str: str) -> None:
        super().__init__(
            f'Invalid UUID format provided: {uuid_str!r}.'
            f' Please ensure the UUID is in a valid format'
            f' (e.g., "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx").'
        )


def empty_uuid() -> UUID:
    return UUID(EMPTY_UUID)


def uuid_from_string(uuid_str: str) -> UUID:
    try:
        return UUID(uuid_str)
    except ValueError as e:
        raise InvalidUUIDError(uuid_str) from e
