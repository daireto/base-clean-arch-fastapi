from resources.domain.value_objects import ResourceUrl


class Resource:
    def __init__(self, resource_url: ResourceUrl):
        self._resource_url = resource_url

    @classmethod
    def create(cls, resource_url: ResourceUrl) -> 'Resource':
        return cls(resource_url)

    @property
    def url(self) -> str:
        return self._resource_url.value
