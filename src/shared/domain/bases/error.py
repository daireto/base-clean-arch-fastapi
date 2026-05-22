from dataclasses import dataclass


@dataclass
class Error(Exception):
    status: int
    title: str
    detail: str
    code: str
    type: str = 'about:blank'
    extra: dict[str, object] | None = None

    def __post_init__(self) -> None:
        super().__init__(self.detail)
