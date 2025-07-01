from abc import ABC, abstractmethod
from uuid import UUID

from odata_v4_query import ODataQueryOptions

from resources.domain.entities import Resource


class ResourceRepositoryABC(ABC):
    @abstractmethod
    async def get_by_id(self, id_: UUID) -> Resource: ...

    @abstractmethod
    async def all(self, odata_options: ODataQueryOptions) -> list[Resource]: ...

    @abstractmethod
    async def save(self, resource: Resource) -> Resource: ...
