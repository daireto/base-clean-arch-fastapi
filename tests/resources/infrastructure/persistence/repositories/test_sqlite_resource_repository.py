import pytest
from odata_v4_query import ODataQueryOptions

from modules.resources.domain.entities import Resource
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)
from modules.resources.infrastructure.persistence.models.sqlite import (
    ResourceModel,
)
from shared.helpers.odata_helper import ODataHelper
from shared.utils.uuid_tools import uuid


@pytest.mark.asyncio
class TestSQLiteResourcesRepository:
    async def test_get_by_id_returns_resource_when_resource_exists(
        self, resource_model: ResourceModel, resources_repo: ResourceRepositoryABC
    ):
        resource = await resources_repo.get_by_id(resource_model.id)

        assert resource is not None
        assert resource.name == resource_model.name
        assert str(resource.url) == str(resource_model.url)
        assert resource.type == resource_model.type

    async def test_get_by_id_returns_none_when_resource_does_not_exist(
        self, resources_repo: ResourceRepositoryABC
    ):
        resource = await resources_repo.get_by_id(uuid())

        assert resource is None

    async def test_all_returns_all_requested_resources(
        self,
        resource_models: list[ResourceModel],
        resources_repo: ResourceRepositoryABC,
    ):
        resources = await resources_repo.all(
            odata_options=ODataQueryOptions(top=10),
        )

        assert len(resources) == len(resource_models)
        assert str(resources[0].url) == str(resource_models[0].url)
        assert str(resources[1].url) == str(resource_models[1].url)

    async def test_create_returns_created_resource(
        self, resources_repo: ResourceRepositoryABC
    ):
        await resources_repo.create(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.com/')
            .with_type('image')
            .build()
        )
        resource = await ResourceModel.one()

        assert resource.name == 'Random Image'
        assert str(resource.url) == 'https://example.com/'
        assert resource.type == 'image'
        assert resource.created_at == resource.updated_at

    async def test_update_returns_updated_resource_when_resource_exists(
        self, resource_model: ResourceModel, resources_repo: ResourceRepositoryABC
    ):
        resource = await resources_repo.update(
            Resource.Builder()
            .with_id(resource_model.id)
            .with_name('Random Image')
            .with_url('https://example.org/')
            .with_type('image')
            .build(),
        )

        assert resource is not None
        assert resource.name == resource_model.name
        assert resource.url_value == 'https://example.org/'

    async def test_update_returns_none_when_resource_does_not_exist(
        self, resources_repo: ResourceRepositoryABC
    ):
        resource = await resources_repo.update(
            Resource.Builder()
            .with_name('Random Image')
            .with_url('https://example.org/')
            .with_type('image')
            .build(),
        )

        assert resource is None

    async def test_delete_returns_none_when_resource_exists(
        self, resource_model: ResourceModel, resources_repo: ResourceRepositoryABC
    ):
        deleted = await resources_repo.delete(resource_model.id)

        assert deleted is None
        assert await ResourceModel.count() == 0

    async def test_delete_returns_none_when_resource_does_not_exist(
        self, resources_repo: ResourceRepositoryABC
    ):
        deleted = await resources_repo.delete(uuid())

        assert deleted is None

    async def test_count_returns_total_number_of_resources(
        self,
        resource_models: list[ResourceModel],
        resources_repo: ResourceRepositoryABC,
    ):
        count = await resources_repo.count()

        assert count == len(resource_models)

    @pytest.mark.usefixtures('resource_models')
    async def test_count_returns_total_number_of_resources_matching_query(
        self, resources_repo: ResourceRepositoryABC
    ):
        odata_helper = ODataHelper.get_from_query(
            '$filter=url eq "https://example.com/"', max_top=100
        )

        count = await resources_repo.count(odata_helper.get_for_counting())

        assert count == 1
