from lagom import Container
from lagom.integrations.fast_api import FastApiIntegration

from resources.domain.repositories import ResourceRepositoryABC
from resources.infrastructure.repositories import SQLiteResourceRepository

container = Container()
container[ResourceRepositoryABC] = SQLiteResourceRepository()
deps = FastApiIntegration(container)
