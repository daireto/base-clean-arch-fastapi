from src.resources.domain.entities import Resource
from src.shared.domain.bases import BaseEntityResponseDTO, BaseRequestDTO


class CreateResourceRequestDTO(BaseRequestDTO):
    name: str
    url: str
    type: str


class ResourceResponseDTO(BaseEntityResponseDTO):
    id: str
    name: str
    url: str
    type: str
    created_at: float
    updated_at: float

    @classmethod
    def from_domain(cls, resource: Resource) -> 'ResourceResponseDTO':
        return cls(
            id=str(resource.id),
            name=resource.name,
            url=resource.url.value,
            type=resource.type.value,
            created_at=resource.created_at,
            updated_at=resource.updated_at,
        )
