from abc import ABC, abstractmethod
from uuid import UUID

from odata_v4_query import ODataQueryOptions
from pydantic import SecretStr

from modules.users.domain.entities import User


class UserRepositoryABC(ABC):
    @abstractmethod
    async def get_by_id(self, id_: UUID) -> User | None: ...

    @abstractmethod
    async def all(self, odata_options: ODataQueryOptions) -> list[User]: ...

    @abstractmethod
    async def create(self, user: User, password: SecretStr) -> User: ...

    @abstractmethod
    async def update(self, user: User) -> User | None: ...

    @abstractmethod
    async def delete(self, id_: UUID) -> None: ...

    @abstractmethod
    async def count(self, odata_options: ODataQueryOptions | None = None) -> int: ...
