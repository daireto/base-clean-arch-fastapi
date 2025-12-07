from abc import ABC
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from shared.helpers.odata_helper import ODataHelper

T = TypeVar('T', bound='ResponseDTO')


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


class PaginatedResponseDTO(ResponseDTO, Generic[T], ABC):
    items: list[T] = Field(..., description='List of returned items matching the query')
    total: int = Field(
        ..., description='Total number of items available in the collection'
    )
    skip: int = Field(..., description='Number of items skipped')
    page: int = Field(..., description='Page number')
    page_size: int = Field(..., description='Number of items returned per page')

    @classmethod
    def from_odata_query_result(
        cls, total: int, items: list[T], odata: ODataHelper
    ) -> 'PaginatedResponseDTO':
        return cls(
            total=total,
            items=items,
            skip=odata.get_skip(),
            page_size=odata.get_top(),
            page=odata.get_page(),
        )
