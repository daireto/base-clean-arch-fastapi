import pytest
import pytest_asyncio
from sqlactive import DBConnection

from resources.domain.entities import Resource
from resources.domain.value_objects import ResourceType, ResourceUrl
from resources.infrastructure.models.sqlite import SQLiteDBModel, SQLiteResourceModel
from resources.infrastructure.repositories.sqlite import SQLiteResourceRepository
from shared import settings

db_conn = DBConnection(settings.DATABASE_URL, echo=False)


@pytest_asyncio.fixture(autouse=True)
async def cleanup():
    await db_conn.init_db(SQLiteDBModel)
    yield
    async with db_conn.async_engine.begin() as conn:
        await conn.run_sync(SQLiteDBModel.metadata.drop_all)


@pytest.mark.asyncio
class TestSQLiteResourcesRepository:
    async def test_return_all_resources_from_database(self):
        await SQLiteResourceModel.create(
            name='Random Image',
            url='https://example.com',
            type='image',
        )
        await SQLiteResourceModel.create(
            name='Random Image',
            url='https://example.org',
            type='image',
        )

        resources = await SQLiteResourceRepository().all()

        expected_resources_count = 2
        assert len(resources) == expected_resources_count
        assert resources[0].url == 'https://example.com'
        assert resources[1].url == 'https://example.org'

    async def test_save_resource_to_database(self):
        await SQLiteResourceRepository().save(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            )
        )

        resource = await SQLiteResourceModel.one()
        assert resource.name == 'Random Image'
        assert resource.url == 'https://example.com'
        assert resource.type == 'image'
