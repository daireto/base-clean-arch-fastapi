from dishka import Provider, Scope

from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.infrastructure.persistence.repositories.sqlite import (
    SQLiteResourceRepository,
)

provider = Provider(scope=Scope.APP)
provider.provide(SQLiteResourceRepository, provides=ResourceRepositoryABC)
