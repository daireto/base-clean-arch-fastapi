class InvalidURL(ValueError):
    def __init__(self, url: str):
        self.url = url
        super().__init__(f'Invalid URL: {url!r}')
