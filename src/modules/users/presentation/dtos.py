from pydantic import EmailStr, Field

from modules.users.domain.entities import User
from modules.users.domain.enums import Gender, Role
from shared.presentation.dtos import EntityResponseDTO, RequestDTO, ResponseDTO
from shared.utils.validation_types import HashedSecretStr


class CreateUserRequestDTO(RequestDTO):
    username: str = Field(..., description='Unique username of the user')
    fullname: str = Field(..., description='Full name of the user')
    email: EmailStr = Field(..., description='Email address of the user')
    gender: Gender = Field(..., description='Gender of the user')
    role: Role = Field(..., description='Role of the user')
    password: HashedSecretStr = Field(
        ..., min_length=8, max_length=80, description='Password of the user'
    )


class UpdateUserRequestDTO(RequestDTO):
    username: str = Field(..., description='Unique username of the user')
    fullname: str = Field(..., description='Full name of the user')
    email: EmailStr = Field(..., description='Email address of the user')
    gender: Gender = Field(..., description='Gender of the user')
    role: Role = Field(..., description='Role of the user')
    password: HashedSecretStr | None = Field(
        None, min_length=8, max_length=80, description='Password of the user'
    )


class PartialUpdateUserRequestDTO(RequestDTO):
    username: str | None = Field(None, description='Unique username of the user')
    fullname: str | None = Field(None, description='Full name of the user')
    email: EmailStr | None = Field(None, description='Email address of the user')
    gender: Gender | None = Field(None, description='Gender of the user')
    role: Role | None = Field(None, description='Role of the user')
    password: HashedSecretStr | None = Field(
        None, min_length=8, max_length=80, description='Password of the user'
    )


class UserDTO(EntityResponseDTO):
    username: str = Field(..., description='Unique username of the user')
    fullname: str = Field(..., description='Full name of the user')
    email: str = Field(..., description='Email address of the user')
    gender: str = Field(..., description='Gender of the user')
    role: str = Field(..., description='Role of the user')

    @classmethod
    def from_entity(cls, user: User) -> 'UserDTO':
        return cls(
            id=str(user.id),
            username=user.username,
            fullname=user.fullname,
            email=user.email,
            gender=user.gender.value,
            role=user.role.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class UserResponseDTO(ResponseDTO):
    user: UserDTO = Field(..., description='User data')

    @classmethod
    def from_entity(cls, user: User) -> 'UserResponseDTO':
        return cls(
            user=UserDTO.from_entity(user),
        )

    @classmethod
    def from_entities(cls, users: list[User]) -> 'list[UserResponseDTO]':
        return [
            cls(
                user=UserDTO.from_entity(user),
            )
            for user in users
        ]
