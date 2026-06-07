from pydantic import Field, HttpUrl

from modules.resources.domain.entities import Resource
from modules.resources.domain.enums import MediaType
from shared.presentation.dtos import EntityResponseDTO, RequestDTO, ResponseDTO


class CreateResourceRequestDTO(RequestDTO):
    name: str = Field(..., description='Name of the resource')
    url: HttpUrl = Field(..., description='URL of the resource')
    type: MediaType = Field(..., description='Media type of the resource')


class UpdateResourceRequestDTO(RequestDTO):
    name: str = Field(..., description='Name of the resource')
    url: HttpUrl = Field(..., description='URL of the resource')
    type: MediaType = Field(..., description='Media type of the resource')


class PartialUpdateResourceRequestDTO(RequestDTO):
    name: str | None = Field(None, description='Name of the resource')
    url: HttpUrl | None = Field(None, description='URL of the resource')
    type: MediaType | None = Field(None, description='Media type of the resource')


class ResourceDTO(EntityResponseDTO):
    name: str = Field(..., description='Name of the resource')
    url: str = Field(..., description='URL of the resource')
    type: str = Field(..., description='Media type of the resource')

    @classmethod
    def from_entity(cls, resource: Resource) -> 'ResourceDTO':
        return cls(
            id=str(resource.id),
            name=resource.name,
            url=resource.url_value,
            type=resource.type,
            created_at=resource.created_at,
            updated_at=resource.updated_at,
        )


class ResourceResponseDTO(ResponseDTO):
    resource: ResourceDTO = Field(..., description='Resource data')

    @classmethod
    def from_entity(cls, resource: Resource) -> 'ResourceResponseDTO':
        return cls(
            resource=ResourceDTO.from_entity(resource),
        )

    @classmethod
    def from_entities(cls, resources: list[Resource]) -> 'list[ResourceResponseDTO]':
        return [
            cls(
                resource=ResourceDTO.from_entity(resource),
            )
            for resource in resources
        ]
