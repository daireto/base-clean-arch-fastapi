from pydantic import EmailStr, Field, SecretStr

from modules.users.domain.entities import User
from modules.users.domain.enums import Gender
from shared.presentation.dtos import EntityResponseDTO, RequestDTO, ResponseDTO


class CreateUserRequestDTO(RequestDTO):
    username: str
    fullname: str
    email: EmailStr
    gender: Gender
    password: SecretStr = Field(..., min_length=8, max_length=80)


class UpdateUserRequestDTO(RequestDTO):
    username: str
    fullname: str
    email: EmailStr
    gender: Gender
    password: SecretStr | None = Field(min_length=8, max_length=80, default=None)


class PartialUpdateUserRequestDTO(RequestDTO):
    username: str | None = None
    fullname: str | None = None
    email: EmailStr | None = None
    gender: Gender | None = None


class UserDTO(EntityResponseDTO):
    id: str
    username: str
    fullname: str
    email: str
    gender: str
    created_at: float
    updated_at: float

    @classmethod
    def from_entity(cls, user: User) -> 'UserDTO':
        return cls(
            id=str(user.id),
            username=user.username,
            fullname=user.fullname,
            email=user.email,
            gender=user.gender.value,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class UserResponseDTO(ResponseDTO):
    user: UserDTO

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
