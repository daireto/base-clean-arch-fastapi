from fastapi import HTTPException, status
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


class BaseError(HTTPException):
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
