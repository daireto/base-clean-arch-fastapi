import pytest
from odata_v4_query import ODataQueryOptions
from pydantic import ValidationError

from modules.resources.application.use_cases.create_resource import (
    CreateResourceCommand,
    CreateResourceHandler,
)
from modules.resources.domain.interfaces.repositories import (
    ResourceRepositoryABC,
)


@pytest.mark.asyncio
class TestCreateResource:
    async def test_returns_created_resource(
        self, resources_repo: ResourceRepositoryABC
    ):
        await CreateResourceHandler(resources_repo).handle(
            CreateResourceCommand(
                name='Random Image',
                url='https://example.com/',
                type='image',
            )
        )
        resources = await resources_repo.all(
            odata_options=ODataQueryOptions(top=100),
        )

        assert len(resources) == 1
        assert str(resources[0].url) == 'https://example.com/'

    async def test_raises_when_resource_url_is_invalid(
        self, resources_repo: ResourceRepositoryABC
    ):
        with pytest.raises(ValidationError):
            await CreateResourceHandler(resources_repo).handle(
                CreateResourceCommand(
                    name='Random Image',
                    url='not-a-valid-url',
                    type='image',
                )
            )

    async def test_raises_when_resource_type_is_not_supported(
        self, resources_repo: ResourceRepositoryABC
    ):
        with pytest.raises(ValidationError):
            await CreateResourceHandler(resources_repo).handle(
                CreateResourceCommand(
                    name='Random Image',
                    url='https://example.com/',
                    type='not-a-valid-type',
                )
            )
