import pytest
from odata_v4_query import ODataQueryOptions

from config import settings
from modules.resources.application.use_cases.create_resource import (
    CreateResourceCommand,
    CreateResourceHandler,
)
from modules.resources.domain.exceptions import ResourceTypeNotSupportedError
from modules.resources.domain.interfaces.repositories import ResourceRepositoryABC
from shared.domain.exceptions import InvalidURLError


@pytest.mark.asyncio
class TestCreateResource:
    async def test_returns_resource_details_after_creating_resource(
        self, repo: ResourceRepositoryABC
    ):
        # Act
        await CreateResourceHandler(repo).handle(
            CreateResourceCommand(
                name='Random Image',
                url='https://example.com',
                type='image',
            )
        )
        resources = await repo.all(
            odata_options=ODataQueryOptions(top=settings.max_records_per_page),
        )

        # Assert
        assert len(resources) == 1
        assert resources[0].url == 'https://example.com'

    async def test_raises_when_resource_url_is_invalid(
        self, repo: ResourceRepositoryABC
    ):
        # Assert
        with pytest.raises(InvalidURLError):
            await CreateResourceHandler(repo).handle(
                CreateResourceCommand(
                    name='Random Image',
                    url='not-a-valid-url',
                    type='image',
                )
            )

    async def test_raises_when_resource_type_is_not_supported(
        self, repo: ResourceRepositoryABC
    ):
        # Assert
        with pytest.raises(ResourceTypeNotSupportedError):
            await CreateResourceHandler(repo).handle(
                CreateResourceCommand(
                    name='Random Image',
                    url='https://example.com',
                    type='not-a-valid-type',
                )
            )
