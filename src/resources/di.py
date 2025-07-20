from lagom import Container
from lagom.integrations.fast_api import FastApiIntegration

from src.resources.domain.repositories import ResourceRepositoryABC
from src.resources.infrastructure.repositories.sqlite import SQLiteResourceRepository

container = Container()
container[ResourceRepositoryABC] = SQLiteResourceRepository()
deps = FastApiIntegration(container)
