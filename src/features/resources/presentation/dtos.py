from features.resources.domain.entities import Resource
from shared.presentation.dto import EntityResponseDTO, RequestDTO, ResponseDTO


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


class ResourcesResponseDTO(ResponseDTO):
    resources: list[ResourceDTO]

    @classmethod
    def from_entities(cls, resources: list[Resource]) -> 'ResourcesResponseDTO':
        return cls(
            resources=[ResourceDTO.from_entity(resource) for resource in resources],
        )
