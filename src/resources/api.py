from fastapi import APIRouter

from src.resources.application.create_resource import (
    CreateResourceCommand,
    CreateResourceHandler,
)
from src.resources.di import deps
from src.resources.domain.repositories import ResourceRepositoryABC
from src.resources.dtos import CreateResourceRequestDTO, ResourceResponseDTO

router = APIRouter()


@router.post('/resources/')
async def create_resource(
    dto: CreateResourceRequestDTO,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> ResourceResponseDTO:
    resource = await CreateResourceHandler(repo).handle(
        CreateResourceCommand(
            name=dto.name,
            url=dto.url,
            type=dto.type,
        )
    )
    return ResourceResponseDTO.from_domain(resource)
