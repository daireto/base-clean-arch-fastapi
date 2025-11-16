from abc import ABC, abstractmethod
from uuid import UUID

from odata_v4_query import ODataQueryOptions

from modules.resources.domain.entities import Resource


class ResourceRepositoryABC(ABC):
    @abstractmethod
    async def get_by_id(self, id_: UUID) -> Resource | None: ...

    @abstractmethod
    async def all(self, odata_options: ODataQueryOptions) -> list[Resource]: ...

    @abstractmethod
    async def create(self, resource: Resource) -> Resource: ...

    @abstractmethod
    async def update(self, resource: Resource) -> Resource | None: ...

    @abstractmethod
    async def delete(self, id_: UUID) -> bool: ...

    @abstractmethod
    async def count(self, odata_options: ODataQueryOptions | None = None) -> bool: ...
