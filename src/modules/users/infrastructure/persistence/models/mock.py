import time
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from modules.users.domain.entities import User
from modules.users.domain.enums import Gender
from shared.utils.validation_types import HashedSecretStr


class MockUserModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    fullname: str
    email: EmailStr
    gender: Gender
    password: HashedSecretStr
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)

    def to_entity(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            fullname=self.fullname,
            email=self.email,
            gender=self.gender,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, entity: User, password: HashedSecretStr) -> 'MockUserModel':
        return cls(
            id=entity.id,
            username=entity.username,
            fullname=entity.fullname,
            email=entity.email,
            gender=entity.gender,
            password=password,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
