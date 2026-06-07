from uuid import UUID, uuid4

from sqlactive import ActiveRecordBaseModel
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from modules.users.domain.entities import User
from modules.users.domain.enums import Gender, Role
from shared.utils.validation_types import HashedSecretStr


class BaseModel(ActiveRecordBaseModel):
    __abstract__ = True


class UserModel(BaseModel):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column()
    fullname: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    role: Mapped[Role] = mapped_column(Enum(Role))
    password: Mapped[str] = mapped_column()

    def to_entity(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            fullname=self.fullname,
            email=self.email,
            gender=self.gender,
            role=self.role,
            created_at=self.created_at.timestamp(),
            updated_at=self.updated_at.timestamp(),
        )

    @classmethod
    def from_entity(cls, entity: User, password: HashedSecretStr) -> 'UserModel':
        return cls(
            id=entity.id,
            username=entity.username,
            fullname=entity.fullname,
            email=entity.email,
            gender=entity.gender,
            role=entity.role,
            password=password.get_secret_value(),
        )
