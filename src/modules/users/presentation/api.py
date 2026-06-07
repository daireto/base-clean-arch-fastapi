from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request, Response, status

from core.config import settings
from modules.users.application.use_cases.create_user import (
    CreateUserCommand,
    CreateUserHandler,
)
from modules.users.application.use_cases.delete_user import (
    DeleteUserCommand,
    DeleteUserHandler,
)
from modules.users.application.use_cases.get_user import (
    GetUserCommand,
    GetUserHandler,
)
from modules.users.application.use_cases.list_users import (
    ListUsersCommand,
    ListUsersHandler,
)
from modules.users.application.use_cases.update_user import (
    PartialUpdateUserCommand,
    UpdateUserCommand,
    UpdateUserHandler,
)
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from modules.users.presentation.dtos import (
    CreateUserRequestDTO,
    PartialUpdateUserRequestDTO,
    UpdateUserRequestDTO,
    UserResponseDTO,
)
from shared.application.instrumentation import (
    CreationUseCaseInstrumentation,
    DeletionUseCaseInstrumentation,
    ListingUseCaseInstrumentation,
    RetrievalUseCaseInstrumentation,
    UpdateUseCaseInstrumentation,
)
from shared.helpers.odata_helper import ODataHelper
from shared.presentation.dtos import PaginatedResponseDTO
from shared.presentation.responses import NoContent

router = APIRouter(
    prefix='/users',
    tags=['users'],
    route_class=DishkaRoute,
)


@router.get('/{id_}')
async def get_user(
    id_: str,
    repo: FromDishka[UserRepositoryABC],
    instrumentation: FromDishka[RetrievalUseCaseInstrumentation],
) -> UserResponseDTO:
    command = GetUserCommand(id=id_)  # type: ignore
    handler = GetUserHandler(
        user_repository=repo,
        instrumentation=instrumentation,
    )

    if result := await handler.handle(command):
        return UserResponseDTO.from_entity(result.unwrap_value())

    raise result.unwrap_error()


@router.get('/')
async def list_users(
    request: Request,
    repo: FromDishka[UserRepositoryABC],
    instrumentation: FromDishka[ListingUseCaseInstrumentation],
) -> PaginatedResponseDTO[UserResponseDTO]:
    odata = ODataHelper.get_from_query(
        query_string=request.url.query,
        max_top=settings.query.max_records_per_page,
    )
    command = ListUsersCommand(
        odata=odata,
    )
    handler = ListUsersHandler(
        user_repository=repo,
        instrumentation=instrumentation,
    )

    if result := await handler.handle_with_count(command):
        users = result.unwrap_value()
        items = UserResponseDTO.from_entities(users)
        return PaginatedResponseDTO.from_odata_query_result(
            users.total_stored, items, odata
        )

    raise result.unwrap_error()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(
    dto: CreateUserRequestDTO,
    repo: FromDishka[UserRepositoryABC],
    instrumentation: FromDishka[CreationUseCaseInstrumentation],
) -> UserResponseDTO:
    command = CreateUserCommand(
        username=dto.username,
        fullname=dto.fullname,
        email=dto.email,
        gender=dto.gender,
        password=dto.password,
    )
    handler = CreateUserHandler(
        user_repository=repo,
        instrumentation=instrumentation,
    )

    if result := await handler.handle(command):
        return UserResponseDTO.from_entity(result.unwrap_value())

    raise result.unwrap_error()


@router.put('/{id_}')
async def update_user(
    id_: str,
    dto: UpdateUserRequestDTO,
    repo: FromDishka[UserRepositoryABC],
    instrumentation: FromDishka[UpdateUseCaseInstrumentation],
) -> UserResponseDTO:
    command = UpdateUserCommand(
        id=id_,  # type: ignore
        username=dto.username,
        fullname=dto.fullname,
        email=dto.email,
        gender=dto.gender,
        password=dto.password,
    )
    handler = UpdateUserHandler(
        user_repository=repo,
        instrumentation=instrumentation,
    )

    if result := await handler.handle(command):
        return UserResponseDTO.from_entity(result.unwrap_value())

    raise result.unwrap_error()


@router.patch('/{id_}')
async def partially_update_user(
    id_: str,
    dto: PartialUpdateUserRequestDTO,
    repo: FromDishka[UserRepositoryABC],
    instrumentation: FromDishka[UpdateUseCaseInstrumentation],
) -> UserResponseDTO:
    command = PartialUpdateUserCommand(
        id=id_,  # type: ignore
        **dto.model_dump(exclude_unset=True),
    )
    handler = UpdateUserHandler(
        user_repository=repo,
        instrumentation=instrumentation,
    )

    if result := await handler.handle_partial(command):
        return UserResponseDTO.from_entity(result.unwrap_value())

    raise result.unwrap_error()


@router.delete('/{id_}')
async def delete_user(
    id_: str,
    repo: FromDishka[UserRepositoryABC],
    instrumentation: FromDishka[DeletionUseCaseInstrumentation],
) -> Response:
    command = DeleteUserCommand(id=id_)  # type: ignore
    handler = DeleteUserHandler(
        user_repository=repo,
        instrumentation=instrumentation,
    )

    if result := await handler.handle(command):
        return NoContent()

    raise result.unwrap_error()
