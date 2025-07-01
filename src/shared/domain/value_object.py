from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class ValueObject:
    value: object

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, value: object) -> bool:
        return (
            self.value == value.value
            if isinstance(value, ValueObject)
            else self.value == value
        )

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __hash__(self) -> int:
        return hash(self.value)
