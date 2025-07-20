from uuid import UUID

EMPTY_UUID = '00000000-0000-0000-0000-000000000000'


def empty_uuid() -> UUID:
    return UUID(EMPTY_UUID)
