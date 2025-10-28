from typing import Generic, TypeVar

T = TypeVar('T')


class AccessedValueOnFailureError(Exception):
    def __init__(self) -> None:
        super().__init__('cannot get value from failed result')


class AccessedErrorOnSuccessError(Exception):
    def __init__(self) -> None:
        super().__init__('cannot get error from successful result')


class Result(Generic[T]):
    def __init__(
        self,
        is_success: bool,
        value: T = None,
        error: Exception | None = None,
    ) -> None:
        self.is_success = is_success
        self.value = value
        self.error = error

    @staticmethod
    def success(value: T = None) -> 'Result[T]':
        return Result(is_success=True, value=value)

    @staticmethod
    def failure(error: Exception) -> 'Result':
        return Result(is_success=False, error=error)

    def get_value_or_raise(self) -> T:
        if not self.is_success:
            raise AccessedValueOnFailureError
        return self.value

    def get_error_or_raise(self) -> Exception:
        if self.is_success:
            raise AccessedErrorOnSuccessError
        return self.error or Exception('unknown error')

    def __bool__(self) -> bool:
        return self.is_success

    def __str__(self) -> str:
        return (
            f'Result('
            f'is_success={self.is_success!r},'
            f' value={self.value!r},'
            f' error={self.error!r})'
        )

    def __repr__(self) -> str:
        return str(self)
