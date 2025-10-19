from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, model_serializer

T = TypeVar('T')


class ValueObject(BaseModel, Generic[T]):
    model_config = ConfigDict(frozen=True)

    value: T

    def __init__(self, value: T) -> None:
        super().__init__(value=value)
        self.validate()

    def get_value(self) -> T:
        return self.value

    def validate(self) -> None:
        pass

    @model_serializer(mode='plain')
    def serialize_model(self) -> T:
        return self.get_value()

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: object) -> bool:
        return (
            self.value == other.value
            if isinstance(other, ValueObject)
            else self.value == other
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.value)
