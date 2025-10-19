from fastapi import status
from fastapi.responses import Response


class EmptyResponse(Response):
    def __init__(self, status_code: int = status.HTTP_204_NO_CONTENT) -> None:
        super().__init__(status_code=status_code)
