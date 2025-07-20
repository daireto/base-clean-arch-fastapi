from fastapi import APIRouter, Request, Response, status
from odata_v4_query import ODataQueryParser

from src.resources.application.create_resource import (
    CreateResourceCommand,
    CreateResourceHandler,
)
from src.resources.application.delete_resource import (
    DeleteResourceCommand,
    DeleteResourceHandler,
)
from src.resources.application.get_resource import (
    GetResourceCommand,
    GetResourceHandler,
)
from src.resources.application.list_resources import ListResourcesHandler
from src.resources.application.update_resource import (
    UpdateResourceCommand,
    UpdateResourceHandler,
)
from src.resources.di import deps
from src.resources.domain.repositories import ResourceRepositoryABC
from src.resources.dtos import CreateResourceRequestDTO, ResourceResponseDTO

router = APIRouter()


@router.get('/resources/{id_}')
async def get_resource(
    id_: str,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> ResourceResponseDTO:
    resource = await GetResourceHandler(repo).handle(GetResourceCommand(id_))
    return ResourceResponseDTO.from_domain(resource)


@router.get('/resources/')
async def list_resources(
    request: Request,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> list[ResourceResponseDTO]:
    parser = ODataQueryParser()
    odata_options = parser.parse_query_string(request.url.query)
    resources = await ListResourcesHandler(repo).handle(odata_options)
    return [ResourceResponseDTO.from_domain(resource) for resource in resources]


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


@router.put('/resources/{id_}')
async def update_resource(
    id_: str,
    dto: CreateResourceRequestDTO,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> ResourceResponseDTO:
    resource = await UpdateResourceHandler(repo).handle(
        UpdateResourceCommand(
            id_=id_,
            name=dto.name,
            url=dto.url,
            type=dto.type,
        )
    )
    return ResourceResponseDTO.from_domain(resource)


@router.delete('/resources/{id_}')
async def delete_resource(
    id_: str,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> Response:
    await DeleteResourceHandler(repo).handle(DeleteResourceCommand(id_))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
