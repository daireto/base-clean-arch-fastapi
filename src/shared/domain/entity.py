import time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.shared.domain.utils import empty_uuid


class Entity(BaseModel):
    id: UUID = Field(default_factory=empty_uuid)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)

    model_config = ConfigDict(frozen=True)
