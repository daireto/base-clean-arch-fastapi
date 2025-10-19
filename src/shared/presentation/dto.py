from abc import ABC

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class DTO(BaseModel, ABC):
    pass


class RequestDTO(DTO, ABC):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ResponseDTO(DTO, ABC):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class EntityResponseDTO(ResponseDTO, ABC):
    id: str
    created_at: float
    updated_at: float
