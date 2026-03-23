import pytest
from odata_v4_query import ODataQueryOptions

from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from modules.resources.infrastructure.persistence.models.sqlite import (
    ResourceModel,
)
from shared.helpers.odata_helper import ODataHelper
from shared.utils.uuid_tools import empty_uuid


@pytest.mark.asyncio
class TestSQLiteResourcesRepository:
    async def test_get_by_id_returns_resource_details_when_resource_exists(
        self, resource_model: ResourceModel, repo: ResourceRepositoryABC
    ):
        # Act
        resource = await repo.get_by_id(resource_model.id)

        # Assert
        assert resource is not None
        assert resource.name == 'Random Image'
        assert str(resource.url) == 'https://example.com/'
        assert resource.type == 'image'

    async def test_get_by_id_returns_none_when_resource_does_not_exist(
        self, repo: ResourceRepositoryABC
    ):
        # Act
        resource = await repo.get_by_id(empty_uuid())

        # Assert
        assert resource is None

    async def test_all_returns_all_requested_resources(
        self, resource_models: list[ResourceModel], repo: ResourceRepositoryABC
    ):
        # Act
        resources = await repo.all(
            odata_options=ODataQueryOptions(top=10),
        )

        # Assert
        assert len(resources) == len(resource_models)
        assert str(resources[0].url) == 'https://example.com/'
        assert str(resources[1].url) == 'https://example.org/'

    async def test_create_returns_resource_details_after_creating_resource(
        self, repo: ResourceRepositoryABC
    ):
        # Act
        await repo.create(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.com/')
            .with_type('image')
            .build()
        )
        resource = await ResourceModel.one()

        # Assert
        assert resource.name == 'Random Image'
        assert str(resource.url) == 'https://example.com/'
        assert resource.type == 'image'
        assert resource.created_at == resource.updated_at

    async def test_update_returns_resource_details_after_updating_resource(
        self, resource_model: ResourceModel, repo: ResourceRepositoryABC
    ):
        # Act
        resource = await repo.update(
            Resource.Builder()
            .with_id(resource_model.id)
            .with_name('Random Image')
            .with_url('https://example.org/')
            .with_type('image')
            .build(),
        )

        # Assert
        assert resource is not None
        assert resource.url_value == 'https://example.org/'

    async def test_update_returns_resource_details_after_creating_resource_when_resource_does_not_exist(
        self, repo: ResourceRepositoryABC
    ):
        # Act
        resource = await repo.update(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.org/')
            .with_type('image')
            .build(),
        )

        # Assert
        assert resource is not None
        assert resource.url_value == 'https://example.org/'
        assert resource.created_at == resource.updated_at

    async def test_delete_returns_none_after_deleting_resource(
        self, resource_model: ResourceModel, repo: ResourceRepositoryABC
    ):
        # Act
        deleted = await repo.delete(resource_model.id)

        # Assert
        assert deleted is None
        assert await ResourceModel.count() == 0

    async def test_delete_returns_none_when_deleting_resource_that_does_not_exist(
        self, repo: ResourceRepositoryABC
    ):
        # Act
        deleted = await repo.delete(empty_uuid())

        # Assert
        assert deleted is None

    async def test_count_returns_total_number_of_resources(
        self, resource_models: list[ResourceModel], repo: ResourceRepositoryABC
    ):
        # Act
        count = await repo.count()

        # Assert
        assert count == len(resource_models)

    @pytest.mark.usefixtures('resource_models')
    async def test_count_returns_total_number_of_resources_matching_query(
        self, repo: ResourceRepositoryABC
    ):
        # Arrange
        odata_helper = ODataHelper.get_from_query(
            '$filter=url eq "https://example.com/"', max_top=100
        )

        # Act
        count = await repo.count(odata_helper.get_for_counting())

        # Assert
        assert count == 1
