from modules.resources.domain.entities import Resource


class ResourceCollection(list[Resource]):
    def __init__(
        self,
        resources: list[Resource],
        total_stored: int | None = None,
    ) -> None:
        super().__init__(resources)
        self.total_stored = total_stored or len(resources)

    def filter_by_type(self, type_: str) -> 'ResourceCollection':
        return ResourceCollection(
            [resource for resource in self if resource.type == type_]
        )

    def filter_by_name(self, name: str) -> 'ResourceCollection':
        return ResourceCollection(
            [resource for resource in self if name.lower() in resource.name.lower()]
        )

    def filter_by_url_domain(self, domain: str) -> 'ResourceCollection':
        return ResourceCollection(
            [resource for resource in self if resource.url.domain_equals_to(domain)]
        )

    def filter_by_url_scheme(self, scheme: str) -> 'ResourceCollection':
        return ResourceCollection(
            [resource for resource in self if resource.url.scheme_equals_to(scheme)]
        )

    def get_created_before(self, timestamp: float) -> 'ResourceCollection':
        return ResourceCollection(
            [resource for resource in self if resource.created_at < timestamp]
        )

    def get_created_after(self, timestamp: float) -> 'ResourceCollection':
        return ResourceCollection(
            [resource for resource in self if resource.created_at > timestamp]
        )

    def get_images(self) -> 'ResourceCollection':
        return self.filter_by_type('image')

    def get_videos(self) -> 'ResourceCollection':
        return self.filter_by_type('video')

    def get_audios(self) -> 'ResourceCollection':
        return self.filter_by_type('audio')

    def get_texts(self) -> 'ResourceCollection':
        return self.filter_by_type('text')

    def get_others(self) -> 'ResourceCollection':
        return self.filter_by_type('other')
