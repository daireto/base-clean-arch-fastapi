from uuid import UUID

from structlog.stdlib import BoundLogger

from shared.domain.bases.entity import Entity
from shared.domain.bases.error import Error


class UseCaseInstrumentation:
    _logger: BoundLogger

    def __init__(self, logger: BoundLogger | None = None) -> None:
        if logger:
            self._logger = logger

    def set_logger(self, logger: BoundLogger) -> None:
        self._logger = logger

    def before(self, *args, **kwargs) -> None:
        pass

    def after(self, *args, **kwargs) -> None:
        pass

    def error(self, error: Exception) -> None:
        pass

    def validation_error(self, error: Error) -> None:
        pass

    def not_found(self, *args, **kwargs) -> None:
        pass


class CreationUseCaseInstrumentation[T: Entity](UseCaseInstrumentation):
    def before(self, entity: T) -> None:
        pass

    def after(self, entity: T) -> None:
        pass


class DeletionUseCaseInstrumentation(UseCaseInstrumentation):
    def before(self, id_: UUID) -> None:
        pass

    def after(self, id_: UUID) -> None:
        pass


class RetrievalUseCaseInstrumentation[T: Entity](UseCaseInstrumentation):
    def before(self, id_: UUID) -> None:
        pass

    def after(self, entity: T) -> None:
        pass

    def not_found(self, id_: UUID) -> None:
        pass


class ListingUseCaseInstrumentation[T: Entity](UseCaseInstrumentation):
    def before(self) -> None:
        pass

    def after(self, entities: list[T]) -> None:
        pass


class UpdateUseCaseInstrumentation[T: Entity](UseCaseInstrumentation):
    def before(self, entity: T) -> None:
        pass

    def after(self, entity: T, created: bool = False) -> None:
        pass

    def not_found(self, id_: UUID) -> None:
        pass
