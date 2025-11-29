from modules.resources.domain.collections import ResourceCollection
from modules.resources.domain.entities import Resource


class TestResourceCollection:
    def test_filter_by_type_returns_only_resources_of_given_type(
        self, resources: list[Resource]
    ):
        # Arrange
        type_ = 'image'
        expected = [resource for resource in resources if resource.type == type_]

        # Act
        collection = ResourceCollection(resources)
        images = collection.filter_by_type(type_)

        # Assert
        assert len(images) == len(expected)
        assert all(resource.type == type_ for resource in images)

    def test_filter_by_name_returns_only_resources_with_given_name(
        self, resources: list[Resource]
    ):
        # Arrange
        name = 'Random Image'
        expected = [resource for resource in resources if name in resource.name]

        # Act
        collection = ResourceCollection(resources)
        filtered = collection.filter_by_name(name)

        # Assert
        assert len(filtered) == len(expected)
        assert all(name in resource.name for resource in filtered)

    def test_filter_by_url_domain_returns_only_resources_with_given_domain(
        self, resources: list[Resource]
    ):
        # Arrange
        domain = 'picsum.photos'
        expected = [
            resource for resource in resources if resource.url.domain_equals_to(domain)
        ]

        # Act
        collection = ResourceCollection(resources)
        filtered = collection.filter_by_url_domain(domain)

        # Assert
        assert len(filtered) == len(expected)
        assert all(resource.url.domain_equals_to(domain) for resource in filtered)

    def test_filter_by_url_scheme_returns_only_resources_with_given_scheme(
        self, resources: list[Resource]
    ):
        # Arrange
        scheme = 'https'
        expected = [
            resource for resource in resources if resource.url.scheme_equals_to(scheme)
        ]

        # Act
        collection = ResourceCollection(resources)
        filtered = collection.filter_by_url_scheme(scheme)

        # Assert
        assert len(filtered) == len(expected)
        assert all(resource.url.scheme_equals_to(scheme) for resource in filtered)

    def test_get_created_before_returns_only_resources_created_before_given_timestamp(
        self, resources: list[Resource]
    ):
        # Arrange
        timestamp = resources[0].created_at
        expected = [
            resource for resource in resources if resource.created_at < timestamp
        ]

        # Act
        collection = ResourceCollection(resources)
        filtered = collection.get_created_before(timestamp)

        # Assert
        assert len(filtered) == len(expected)
        assert all(resource.created_at < timestamp for resource in filtered)

    def test_get_created_after_returns_only_resources_created_after_given_timestamp(
        self, resources: list[Resource]
    ):
        # Arrange
        timestamp = resources[0].created_at
        expected = [
            resource for resource in resources if resource.created_at > timestamp
        ]

        # Act
        collection = ResourceCollection(resources)
        filtered = collection.get_created_after(timestamp)

        # Assert
        assert len(filtered) == len(expected)
        assert all(resource.created_at > timestamp for resource in filtered)

    def test_get_images_returns_only_images(self, resources: list[Resource]):
        # Arrange
        expected = [resource for resource in resources if resource.type == 'image']

        # Act
        collection = ResourceCollection(resources)
        images = collection.get_images()

        # Assert
        assert len(images) == len(expected)
        assert all(resource.type == 'image' for resource in images)

    def test_get_videos_returns_only_videos(self, resources: list[Resource]):
        # Arrange
        expected = [resource for resource in resources if resource.type == 'video']

        # Act
        collection = ResourceCollection(resources)
        videos = collection.get_videos()

        # Assert
        assert len(videos) == len(expected)
        assert all(resource.type == 'video' for resource in videos)

    def test_get_audios_returns_only_audios(self, resources: list[Resource]):
        # Arrange
        expected = [resource for resource in resources if resource.type == 'audio']

        # Act
        collection = ResourceCollection(resources)
        audios = collection.get_audios()

        # Assert
        assert len(audios) == len(expected)
        assert all(resource.type == 'audio' for resource in audios)

    def test_get_texts_returns_only_texts(self, resources: list[Resource]):
        # Arrange
        expected = [resource for resource in resources if resource.type == 'text']

        # Act
        collection = ResourceCollection(resources)
        texts = collection.get_texts()

        # Assert
        assert len(texts) == len(expected)
        assert all(resource.type == 'text' for resource in texts)

    def test_get_others_returns_only_others(self, resources: list[Resource]):
        # Arrange
        expected = [resource for resource in resources if resource.type == 'other']

        # Act
        collection = ResourceCollection(resources)
        others = collection.get_others()

        # Assert
        assert len(others) == len(expected)
        assert all(resource.type == 'other' for resource in others)

    def test_sort_by_name_returns_resources_sorted_by_name(self, resources: list[Resource]):
        # Act
        collection = ResourceCollection(resources)
        sorted_ = collection.sort_by_name()

        # Assert
        assert sorted_ == sorted(resources, key=lambda resource: resource.name)

    def test_sort_by_created_at_returns_resources_sorted_by_created_at(
        self, resources: list[Resource]
    ):
        # Act
        collection = ResourceCollection(resources)
        sorted_ = collection.sort_by_created_at()

        # Assert
        assert sorted_ == sorted(resources, key=lambda resource: resource.created_at)
