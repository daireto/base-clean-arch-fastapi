from uuid import UUID

from modules.resources.domain.error_codes import ErrorCode
from shared.domain.bases.error import Error


class ResourceNotFoundError(Error):
    def __init__(self, id_: UUID) -> None:
        self.id = id_
        super().__init__(
            status=404,
            title='Resource Not Found',
            detail='The resource was not found.',
            code=ErrorCode.RESOURCE_NOT_FOUND,
            extra={'resource_id': id_},
        )
