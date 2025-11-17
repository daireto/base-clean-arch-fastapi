from fastapi import APIRouter, Request, Response

from modules.resources.application.use_cases.create_resource import (
    CreateResourceCommand,
    CreateResourceHandler,
)
from modules.resources.application.use_cases.delete_resource import (
    DeleteResourceCommand,
    DeleteResourceHandler,
)
from modules.resources.application.use_cases.get_resource import (
    GetResourceCommand,
    GetResourceHandler,
)
from modules.resources.application.use_cases.list_resources import (
    ListResourcesCommand,
    ListResourcesHandler,
)
from modules.resources.application.use_cases.update_resource import (
    UpdateResourceCommand,
    UpdateResourceHandler,
)
from modules.resources.di import deps
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.presentation.dtos import (
    CreateResourceRequestDTO,
    ResourceResponseDTO,
)
from shared.domain.helpers.odata_helper import ODataHelper
from shared.presentation.dtos import PaginatedResponseDTO
from shared.presentation.responses import EmptyResponse
from shared.utils.uuid_tools import uuid_from_string

router = APIRouter()


@router.get('/resources/{id_}')
async def get_resource(
    id_: str,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> ResourceResponseDTO:
    uuid_id = uuid_from_string(id_)
    command = GetResourceCommand(id=uuid_id)
    if result := await GetResourceHandler(repo).handle(command):
        return ResourceResponseDTO.from_entity(result.unwrap_value())
    raise result.unwrap_error()


@router.get('/resources/')
async def list_resources(
    request: Request,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> PaginatedResponseDTO[ResourceResponseDTO]:
    odata = ODataHelper.get_from_query(request.url.query)
    command = ListResourcesCommand(
        odata=odata,
    )
    if result := await ListResourcesHandler(repo).handle_with_count(command):
        resources, total = result.unwrap_value()
        items = ResourceResponseDTO.from_entities(resources)
        return PaginatedResponseDTO.from_odata_query_result(total, items, odata)
    raise result.unwrap_error()


@router.post('/resources/')
async def create_resource(
    dto: CreateResourceRequestDTO,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> ResourceResponseDTO:
    command = CreateResourceCommand(name=dto.name, url=dto.url, type=dto.type)
    if result := await CreateResourceHandler(repo).handle(command):
        return ResourceResponseDTO.from_entity(result.unwrap_value())
    raise result.unwrap_error()


@router.put('/resources/{id_}')
async def update_resource(
    id_: str,
    dto: CreateResourceRequestDTO,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> ResourceResponseDTO:
    uuid_id = uuid_from_string(id_)
    command = UpdateResourceCommand(
        id=uuid_id,
        name=dto.name,
        url=dto.url,
        type=dto.type,
    )
    if result := await UpdateResourceHandler(repo).handle(command):
        return ResourceResponseDTO.from_entity(result.unwrap_value())
    raise result.unwrap_error()


@router.delete('/resources/{id_}')
async def delete_resource(
    id_: str,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> Response:
    command = DeleteResourceCommand(id=uuid_from_string(id_))
    if result := await DeleteResourceHandler(repo).handle(command):
        return EmptyResponse()
    raise result.unwrap_error()
