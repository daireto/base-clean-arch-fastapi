import pytest

from shared.domain.bases.entity import MockEntity


@pytest.fixture
def entities() -> list[MockEntity]:
    return [
        MockEntity(foo='bar'),
        MockEntity(foo='baz'),
        MockEntity(foo='qux'),
    ]
