from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request, Response, status

from config import settings
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
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from modules.resources.infrastructure.instrumentation.use_cases.create_resource import (
    CreateResourceInstrumentation,
)
from modules.resources.infrastructure.instrumentation.use_cases.delete_resource import (
    DeleteResourceInstrumentation,
)
from modules.resources.infrastructure.instrumentation.use_cases.get_resource import (
    GetResourceInstrumentation,
)
from modules.resources.infrastructure.instrumentation.use_cases.list_resources import (
    ListResourcesInstrumentation,
)
from modules.resources.infrastructure.instrumentation.use_cases.update_resource import (
    UpdateResourceInstrumentation,
)
from modules.resources.presentation.dtos import (
    CreateResourceRequestDTO,
    ResourceResponseDTO,
)
from shared.helpers.odata_helper import ODataHelper
from shared.presentation.dtos import PaginatedResponseDTO
from shared.presentation.responses import NoContent
from shared.utils.uuid_tools import uuid_from_string

router = APIRouter(
    prefix='/resources',
    tags=['resources'],
    route_class=DishkaRoute,
)


@router.get('/{id_}')
async def get_resource(
    request: Request,
    id_: str,
    repo: FromDishka[ResourceRepositoryABC],
) -> ResourceResponseDTO:
    uuid_id = uuid_from_string(id_)
    command = GetResourceCommand(id=uuid_id)
    handler = GetResourceHandler(
        resource_repository=repo,
        instrumentation=GetResourceInstrumentation(
            logger=request.app.state.get_child_logger('resources.get'),
        ),
    )

    if result := await handler.handle(command):
        return ResourceResponseDTO.from_entity(result.unwrap_value())

    raise result.unwrap_error()


@router.get('/')
async def list_resources(
    request: Request,
    repo: FromDishka[ResourceRepositoryABC],
) -> PaginatedResponseDTO[ResourceResponseDTO]:
    odata = ODataHelper.get_from_query(
        query_string=request.url.query,
        max_top=settings.query.max_records_per_page,
    )
    command = ListResourcesCommand(
        odata=odata,
    )
    handler = ListResourcesHandler(
        resource_repository=repo,
        instrumentation=ListResourcesInstrumentation(
            logger=request.app.state.get_child_logger('resources.list'),
        ),
    )

    if result := await handler.handle_with_count(command):
        resources = result.unwrap_value()
        items = ResourceResponseDTO.from_entities(resources)
        return PaginatedResponseDTO.from_odata_query_result(
            resources.total_stored, items, odata
        )

    raise result.unwrap_error()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_resource(
    request: Request,
    dto: CreateResourceRequestDTO,
    repo: FromDishka[ResourceRepositoryABC],
) -> ResourceResponseDTO:
    command = CreateResourceCommand(name=dto.name, url=dto.url, type=dto.type)
    handler = CreateResourceHandler(
        resource_repository=repo,
        instrumentation=CreateResourceInstrumentation(
            logger=request.app.state.get_child_logger('resources.create'),
        ),
    )

    if result := await handler.handle(command):
        return ResourceResponseDTO.from_entity(result.unwrap_value())

    raise result.unwrap_error()


@router.put('/{id_}')
async def update_resource(
    request: Request,
    id_: str,
    dto: CreateResourceRequestDTO,
    repo: FromDishka[ResourceRepositoryABC],
) -> ResourceResponseDTO:
    uuid_id = uuid_from_string(id_)
    command = UpdateResourceCommand(
        id=uuid_id,
        name=dto.name,
        url=dto.url,
        type=dto.type,
    )
    handler = UpdateResourceHandler(
        resource_repository=repo,
        instrumentation=UpdateResourceInstrumentation(
            logger=request.app.state.get_child_logger('resources.update'),
        ),
    )

    if result := await handler.handle(command):
        return ResourceResponseDTO.from_entity(result.unwrap_value())

    raise result.unwrap_error()


@router.delete('/{id_}')
async def delete_resource(
    request: Request,
    id_: str,
    repo: FromDishka[ResourceRepositoryABC],
) -> Response:
    command = DeleteResourceCommand(id=uuid_from_string(id_))
    handler = DeleteResourceHandler(
        resource_repository=repo,
        instrumentation=DeleteResourceInstrumentation(
            logger=request.app.state.get_child_logger('resources.delete'),
        ),
    )

    if result := await handler.handle(command):
        return NoContent()

    raise result.unwrap_error()
