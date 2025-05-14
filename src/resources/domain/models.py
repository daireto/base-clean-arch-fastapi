class Resource:
    def __init__(self, resource_url: str):
        self._resource_url = resource_url

    @classmethod
    def create(cls, resource_url: str) -> 'Resource':
        return cls(resource_url)

    def url(self) -> str:
        return self._resource_url
