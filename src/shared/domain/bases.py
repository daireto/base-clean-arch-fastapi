from fastapi import status
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseDTO(BaseModel):
    pass


class BaseRequestDTO(BaseDTO):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class BaseResponseDTO(BaseDTO):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class BaseEntityResponseDTO(BaseResponseDTO):
    id: str
    created_at: float
    updated_at: float


class BaseError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)
