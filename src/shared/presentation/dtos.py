from abc import ABC

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from shared.helpers.odata_helper import ODataHelper


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
    id: str = Field(..., description='Unique identifier of the entity')
    created_at: float = Field(
        ..., description='Unix timestamp of when the entity was created'
    )
    updated_at: float = Field(
        ..., description='Unix timestamp of when the entity was last updated'
    )


class PaginatedResponseDTO[T: ResponseDTO](ResponseDTO, ABC):
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


class ServerHealthResponse(BaseModel):
    message: str = Field(..., description='"ok" if healthy, error message otherwise.')
    healthy: bool = Field(..., description='Health status')
