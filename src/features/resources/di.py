from lagom import Container
from lagom.integrations.fast_api import FastApiIntegration

from features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from features.resources.infrastructure.persistence.repositories.sqlite import (
    SQLiteResourceRepository,
)


def configure_dependencies(container: Container) -> None:
    container[ResourceRepositoryABC] = SQLiteResourceRepository()


container = Container()
configure_dependencies(container)
deps = FastApiIntegration(container)
