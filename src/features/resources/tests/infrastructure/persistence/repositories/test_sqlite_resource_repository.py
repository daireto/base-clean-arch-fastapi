import pytest
import pytest_asyncio
from odata_v4_query import ODataQueryOptions
from sqlactive import DBConnection

from features.resources.domain.entities import Resource
from features.resources.infrastructure.persistence.models.sqlite import (
    SQLiteResourceModel,
    SQLiteResourcesBaseModel,
)
from features.resources.infrastructure.persistence.repositories.sqlite import (
    SQLiteResourceRepository,
)
from shared.utils.uuid_tools import empty_uuid

mock_conn = DBConnection('sqlite+aiosqlite:///:memory:', echo=False)


@pytest_asyncio.fixture(autouse=True)
async def setup_and_clean_db():
    await mock_conn.init_db(SQLiteResourcesBaseModel)
    yield
    async with mock_conn.async_engine.begin() as conn:
        await conn.run_sync(SQLiteResourcesBaseModel.metadata.drop_all)


@pytest_asyncio.fixture
async def resource_model() -> SQLiteResourceModel:
    return await SQLiteResourceModel.from_entity(
        Resource.Builder()
        .with_name('Random Image')
        .with_url('https://example.com')
        .with_type('image')
        .build()
    ).save()


@pytest_asyncio.fixture
async def resource_models() -> list[SQLiteResourceModel]:
    return [
        await SQLiteResourceModel.from_entity(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.com')
            .with_type('image')
            .build()
        ).save(),
        await SQLiteResourceModel.from_entity(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.org')
            .with_type('image')
            .build()
        ).save(),
    ]


@pytest.mark.asyncio
class TestSQLiteResourcesRepository:
    async def test_get_by_id_returns_resource_details_when_resource_exists(
        self, resource_model: SQLiteResourceModel
    ):
        # Act
        resource = await SQLiteResourceRepository().get_by_id(resource_model.id)

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

    async def test_all_returns_all_requested_resources(
        self, resource_models: list[SQLiteResourceModel]
    ):
        # Act
        resources = await SQLiteResourceRepository().all(
            odata_options=ODataQueryOptions(top=10),
        )

        # Assert
        assert len(resources) == len(resource_models)
        assert resources[0].url == 'https://example.com'
        assert resources[1].url == 'https://example.org'

    async def test_create_returns_resource_details_after_creating_resource(self):
        # Act
        await SQLiteResourceRepository().create(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.com')
            .with_type('image')
            .build()
        )
        resource = await SQLiteResourceModel.one()

        # Assert
        assert resource.name == 'Random Image'
        assert resource.url == 'https://example.com'
        assert resource.type == 'image'
        assert resource.created_at == resource.updated_at

    async def test_update_returns_resource_details_after_updating_resource(
        self, resource_model: SQLiteResourceModel
    ):
        # Act
        resource = await SQLiteResourceRepository().update(
            Resource.Builder()
            .with_id(resource_model.id)
            .with_name('Random Image')
            .with_url('https://example.org')
            .with_type('image')
            .build(),
        )

        # Assert
        assert resource is not None
        assert resource.url_value == 'https://example.org'

    async def test_update_returns_none_when_resource_does_not_exist(self):
        # Act
        resource = await SQLiteResourceRepository().update(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.org')
            .with_type('image')
            .build(),
        )

        # Assert
        assert resource is None

    async def test_delete_returns_true_after_deleting_resource(
        self, resource_model: SQLiteResourceModel
    ):
        # Act
        deleted = await SQLiteResourceRepository().delete(resource_model.id)

        # Assert
        assert deleted
        assert await SQLiteResourceModel.count() == 0

    async def test_delete_returns_false_when_resource_does_not_exist(self):
        # Act
        deleted = await SQLiteResourceRepository().delete(empty_uuid())

        # Assert
        assert not deleted
