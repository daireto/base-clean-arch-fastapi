from modules.resources.domain.entities import Resource
from shared.presentation.dtos import EntityResponseDTO, RequestDTO, ResponseDTO


class CreateResourceRequestDTO(RequestDTO):
    name: str
    url: str
    type: str


class ResourceDTO(EntityResponseDTO):
    id: str
    name: str
    url: str
    type: str
    created_at: float
    updated_at: float

    @classmethod
    def from_entity(cls, resource: Resource) -> 'ResourceDTO':
        return cls(
            id=str(resource.id),
            name=resource.name,
            url=resource.url_value,
            type=resource.type_value,
            created_at=resource.created_at,
            updated_at=resource.updated_at,
        )


class ResourceResponseDTO(ResponseDTO):
    resource: ResourceDTO

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
