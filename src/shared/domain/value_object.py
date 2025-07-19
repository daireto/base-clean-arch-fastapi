from pydantic import BaseModel, ConfigDict


class ValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: object

    def __init__(self, value: object) -> None:
        super().__init__(value=value)
        self.validate()

    def validate(self) -> None:
        pass

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
