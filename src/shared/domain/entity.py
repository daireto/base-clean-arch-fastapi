import time
from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Entity(BaseModel, ABC):
    id: UUID = Field(default_factory=uuid4)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)

    def set_id(self, id_: UUID) -> None:
        self.id = id_

    class Builder(ABC):
        def __init__(self) -> None:
            self._id = uuid4()

        def with_id(self, id_: UUID):  # noqa: ANN201
            self._id = id_
            return self

        @abstractmethod
        def build(self): ...  # noqa: ANN201

        @abstractmethod
        def build_with_defaults(self): ...  # noqa: ANN201
