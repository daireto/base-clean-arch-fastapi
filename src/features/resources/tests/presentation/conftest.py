from typing import cast

import pytest

from src.features.resources.di import container
from src.features.resources.domain.interfaces.repositories import ResourceRepositoryABC
from src.features.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)


@pytest.fixture(scope='package')
def repo() -> MockResourceRepository:
    repository = MockResourceRepository()
    if repository := container.resolve(ResourceRepositoryABC):
        return cast('MockResourceRepository', repository)
    container[ResourceRepositoryABC] = repository
    return repository
