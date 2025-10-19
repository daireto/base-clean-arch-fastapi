import pytest
from odata_v4_query import ODataQueryOptions

from src.core.config import settings
from src.features.resources.application.use_cases.create_resource import (
    CreateResourceCommand,
    CreateResourceHandler,
)
from src.features.resources.domain.errors import ResourceTypeNotSupportedError
from src.features.resources.infrastructure.persistence.repositories.mock import (
    MockResourceRepository,
)
from src.shared.domain.errors import InvalidURLError


@pytest.mark.asyncio
class TestCreateResource:
    async def test_returns_resource_details_after_creating_resource(self):
        # Arrange
        repo = MockResourceRepository()

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

    async def test_raises_when_resource_url_is_invalid(self):
        # Arrange
        repo = MockResourceRepository()

        # Assert
        with pytest.raises(InvalidURLError):
            await CreateResourceHandler(repo).handle(
                CreateResourceCommand(
                    name='Random Image',
                    url='not-a-valid-url',
                    type='image',
                )
            )

    async def test_raises_when_resource_type_is_not_supported(self):
        # Arrange
        repo = MockResourceRepository()

        # Assert
        with pytest.raises(ResourceTypeNotSupportedError):
            await CreateResourceHandler(repo).handle(
                CreateResourceCommand(
                    name='Random Image',
                    url='https://example.com',
                    type='not-a-valid-type',
                )
            )
