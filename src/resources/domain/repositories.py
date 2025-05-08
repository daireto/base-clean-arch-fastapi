from abc import ABC, abstractmethod

from resources.domain.models import Resource


class ResourcesRepository(ABC):
    @abstractmethod
    def get(self) -> Resource: ...
