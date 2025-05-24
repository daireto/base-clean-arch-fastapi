from sqlmodel import Session
from resources.domain.models import Resource
from resources.domain.value_objects import ResourceUrl
from resources.infrastructure.repositories import SQLModelResourcesRepository


class TestSQLModelResourcesRepository:
    def test_save_resource_to_database(self) -> None:
        repo = SQLModelResourcesRepository()
        repo.save(Resource(ResourceUrl(value='https://example.com')))
        with Session(engine) as session:
            stmt = select(Resource)
            resource = session.exec(stmt).first()
            assert resource.url == 'https://example.com'
