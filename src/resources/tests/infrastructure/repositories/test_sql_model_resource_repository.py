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
    @pytest.fixture(autouse=True, scope='function')
    def cleanup(self):
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_save_resource_to_database(self) -> None:
        repo = SQLModelResourcesRepository()

        repo.save(Resource(ResourceUrl(value='https://example.com')))

        with Session(engine) as session:
            resource = session.exec(select(ResourceModel)).one()
            assert resource.url == 'https://example.com'

    def test_return_all_resources_from_database(self) -> None:
        with Session(engine) as session:
            session.add(ResourceModel(url='https://example.com'))
            session.add(ResourceModel(url='https://example.org'))
            session.commit()

        resources = SQLModelResourcesRepository().all()

        assert len(resources) == 2
        assert resources[0].url == 'https://example.com'
        assert resources[1].url == 'https://example.org'
