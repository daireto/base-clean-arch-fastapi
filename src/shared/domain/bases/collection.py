from typing import Self

from shared.domain.bases.entity import Entity


class Collection[T: Entity](list[T]):
    def __init__(
        self,
        items: list[T],
        total_stored: int | None = None,
    ) -> None:
        super().__init__(items)
        self.total_stored = total_stored or len(items)

    def get_created_before(self, timestamp: float) -> Self:
        return self.__class__([item for item in self if item.created_at < timestamp])

    def get_created_after(self, timestamp: float) -> Self:
        return self.__class__([item for item in self if item.created_at > timestamp])

    def sort_by_created_at(self) -> Self:
        return self.__class__(sorted(self, key=lambda item: item.created_at))
