import time
from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from shared.domain.bases.value_object import ValueObject


class Entity(BaseModel, ABC):
    id: UUID = Field(default_factory=uuid4)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)

    def update(self, data: BaseModel | dict[str, Any]):  # noqa: ANN201
        if isinstance(data, BaseModel):
            dumped_data = data.model_dump(exclude_unset=True)
        else:
            dumped_data = data

        dumped_data['updated_at'] = time.time()
        updated_data = {**self.model_dump(), **dumped_data}
        new_model = {}

        for key, value in updated_data.items():
            if not hasattr(self, key):
                continue
            attr = getattr(self, key)
            if isinstance(attr, ValueObject):
                new_model[key] = attr.__class__(value=value)
            else:
                new_model[key] = value

        return self.model_validate(new_model)

    class Builder(ABC):
        def __init__(self) -> None:
            self._id = uuid4()

        def with_id(self, id_: UUID):  # noqa: ANN201
            self._id = id_
            return self

        @abstractmethod
        def build(self): ...  # noqa: ANN201
