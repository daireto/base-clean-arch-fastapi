import pytest
import pytest_asyncio
from odata_v4_query import ODataQueryOptions
from sqlactive import DBConnection

from src.features.resources.domain.entities import Resource
from src.features.resources.domain.value_objects import ResourceType, ResourceUrl
from src.features.resources.infrastructure.persistence.models.sqlite import (
    SQLiteResourceModel,
    SQLiteResourcesBaseModel,
)
from src.features.resources.infrastructure.persistence.repositories.sqlite import (
    SQLiteResourceRepository,
)
from src.shared.utils import empty_uuid

mock_conn = DBConnection('sqlite+aiosqlite:///:memory:', echo=False)


@pytest_asyncio.fixture(autouse=True)
async def setup_and_clean_db():
    await mock_conn.init_db(SQLiteResourcesBaseModel)
    yield
    async with mock_conn.async_engine.begin() as conn:
        await conn.run_sync(SQLiteResourcesBaseModel.metadata.drop_all)


@pytest.mark.asyncio
class TestSQLiteResourcesRepository:
    async def test_get_by_id_returns_resource_details_when_resource_exists(self):
        # Arrange
        resource = await SQLiteResourceModel.create(
            name='Random Image',
            url='https://example.com',
            type='image',
        )

        # Act
        resource = await SQLiteResourceRepository().get_by_id(resource.id)

        # Assert
        assert resource is not None
        assert resource.name == 'Random Image'
        assert resource.url == 'https://example.com'
        assert resource.type == 'image'

    async def test_get_by_id_returns_none_when_resource_does_not_exist(self):
        # Act
        resource = await SQLiteResourceRepository().get_by_id(empty_uuid())

        # Assert
        assert resource is None

    async def test_all_returns_all_requested_resources(self):
        # Arrange
        expected_resources_count = 2
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

        # Act
        resources = await SQLiteResourceRepository().all(
            odata_options=ODataQueryOptions(top=10),
        )

        # Assert
        assert len(resources) == expected_resources_count
        assert resources[0].url == 'https://example.com'
        assert resources[1].url == 'https://example.org'

    async def test_create_returns_resource_details_after_creating_resource(self):
        # Act
        await SQLiteResourceRepository().create(
            Resource(
                name='Random Image',
                url=ResourceUrl(value='https://example.com'),
                type=ResourceType(value='image'),
            )
        )
        resource = await SQLiteResourceModel.one()

        # Assert
        assert resource.name == 'Random Image'
        assert resource.url == 'https://example.com'
        assert resource.type == 'image'
        assert resource.created_at == resource.updated_at

    async def test_update_returns_resource_details_after_updating_resource(self):
        # Arrange
        resource = await SQLiteResourceModel.create(
            name='Random Image',
            url='https://example.com',
            type='image',
        )

        # Act
        resource = await SQLiteResourceRepository().update(
            Resource(
                id=resource.id,
                name='Random Image',
                url=ResourceUrl(value='https://example.org'),
                type=ResourceType(value='image'),
            )
        )

        # Assert
        assert resource is not None
        assert resource.url_value == 'https://example.org'

    async def test_update_returns_none_when_resource_does_not_exist(self):
        # Act
        resource = await SQLiteResourceRepository().update(
            Resource(
                id=empty_uuid(),
                name='Random Image',
                url=ResourceUrl(value='https://example.org'),
                type=ResourceType(value='image'),
            )
        )

        # Assert
        assert resource is None

    async def test_delete_returns_true_after_deleting_resource(self):
        # Arrange
        resource = await SQLiteResourceModel.create(
            name='Random Image',
            url='https://example.com',
            type='image',
        )

        # Act
        deleted = await SQLiteResourceRepository().delete(resource.id)

        # Assert
        assert deleted
        assert await SQLiteResourceModel.count() == 0

    async def test_delete_returns_false_when_resource_does_not_exist(self):
        # Act
        deleted = await SQLiteResourceRepository().delete(empty_uuid())

        # Assert
        assert not deleted
