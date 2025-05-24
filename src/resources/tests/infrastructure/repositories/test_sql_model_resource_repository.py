import pytest
from sqlmodel import SQLModel, Session, select
from resources.domain.models import Resource
from resources.domain.value_objects import ResourceUrl
from resources.infrastructure.repositories import (
    ResourceModel,
    SQLModelResourcesRepository,
    engine,
)


class TestSQLModelResourcesRepository:
    @pytest.fixture(autouse=True)
    def cleanup(self):
        yield
        SQLModel.metadata.drop_all(engine)

    def test_save_resource_to_database(self) -> None:
        repo = SQLModelResourcesRepository()

        repo.save(Resource(ResourceUrl(value='https://example.com')))

        with Session(engine) as session:
            stmt = select(ResourceModel)
            resource = session.exec(stmt).first()
            assert resource.url == 'https://example.com'
