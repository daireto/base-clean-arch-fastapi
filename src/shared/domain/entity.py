import time
from abc import ABC
from uuid import UUID

from pydantic import BaseModel, Field

from src.shared.utils import empty_uuid


class Entity(BaseModel, ABC):
    id: UUID = Field(default_factory=empty_uuid)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
