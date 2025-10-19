from fastapi import APIRouter, Request, Response
from odata_v4_query import ODataQueryParser

from src.core.responses import EmptyResponse
from src.features.resources.application.use_cases.create_resource import (
    CreateResourceCommand,
    CreateResourceHandler,
)
from src.features.resources.application.use_cases.delete_resource import (
    DeleteResourceCommand,
    DeleteResourceHandler,
)
from src.features.resources.application.use_cases.get_resource import (
    GetResourceCommand,
    GetResourceHandler,
)
from src.features.resources.application.use_cases.list_resources import (
    ListResourcesHandler,
)
from src.features.resources.application.use_cases.update_resource import (
    UpdateResourceCommand,
    UpdateResourceHandler,
)
from src.features.resources.di import deps
from src.features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from src.features.resources.presentation.dtos import (
    CreateResourceRequestDTO,
    ResourceResponseDTO,
    ResourcesResponseDTO,
)
from src.shared.presentation.exception_mapper import to_http_exception
from src.shared.utils import uuid_from_string

router = APIRouter()


@router.get('/resources/{id_}')
async def get_resource(
    id_: str,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> ResourceResponseDTO:
    uuid_id = uuid_from_string(id_)
    command = GetResourceCommand(id=uuid_id)
    if result := await GetResourceHandler(repo).handle(command):
        return ResourceResponseDTO.from_entity(result.get_value_or_raise())
    raise to_http_exception(result.get_error_or_raise())


@router.get('/resources/')
async def list_resources(
    request: Request,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> ResourcesResponseDTO:
    parser = ODataQueryParser()
    odata_options = parser.parse_query_string(request.url.query)
    if result := await ListResourcesHandler(repo).handle(odata_options):
        return ResourcesResponseDTO.from_entities(result.get_value_or_raise())
    raise to_http_exception(result.get_error_or_raise())


@router.post('/resources/')
async def create_resource(
    dto: CreateResourceRequestDTO,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> ResourceResponseDTO:
    command = CreateResourceCommand(name=dto.name, url=dto.url, type=dto.type)
    if result := await CreateResourceHandler(repo).handle(command):
        return ResourceResponseDTO.from_entity(result.get_value_or_raise())
    raise to_http_exception(result.get_error_or_raise())


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
        return ResourceResponseDTO.from_entity(result.get_value_or_raise())
    raise to_http_exception(result.get_error_or_raise())


@router.delete('/resources/{id_}')
async def delete_resource(
    id_: str,
    repo: ResourceRepositoryABC = deps.depends(ResourceRepositoryABC),
) -> Response:
    command = DeleteResourceCommand(id=uuid_from_string(id_))
    if result := await DeleteResourceHandler(repo).handle(command):
        return EmptyResponse()
    raise to_http_exception(result.get_error_or_raise())
