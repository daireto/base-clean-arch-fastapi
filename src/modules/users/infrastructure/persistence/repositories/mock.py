from uuid import UUID

from odata_v4_query import ODataQueryOptions
from pydantic import SecretStr

from modules.users.domain.entities import User
from modules.users.domain.interfaces.repositories import (
    UserRepositoryABC,
)
from modules.users.infrastructure.persistence.models.mock import (
    MockUserModel,
)


class MockUserRepository(UserRepositoryABC):
    def __init__(self) -> None:
        self._storage: dict[UUID, MockUserModel] = {}

    async def get_by_id(self, id_: UUID) -> User | None:
        user = self._storage.get(id_)
        return user.to_entity() if user else None

    async def all(self, odata_options: ODataQueryOptions) -> list[User]:
        users = list(self._storage.values())

        if odata_options.skip:
            users = users[odata_options.skip :]
        if odata_options.top:
            users = users[: odata_options.top]

        return [model.to_entity() for model in users]

    async def create(self, user: User, password: SecretStr) -> User:
        _ = password
        model = MockUserModel.from_entity(user)
        self._storage[model.id] = model
        return model.to_entity()

    async def update(self, user: User) -> User | None:
        model = self._storage.get(user.id)
        if not model:
            return None

        model = MockUserModel.from_entity(user)
        self._storage[user.id] = model
        model.id = user.id

        return model.to_entity()

    async def delete(self, id_: UUID) -> None:
        user = self._storage.get(id_)
        if not user:
            return

        del self._storage[id_]

    async def count(self, _: ODataQueryOptions | None = None) -> int:
        return len(self._storage)

    def clear(self) -> None:
        self._storage.clear()
