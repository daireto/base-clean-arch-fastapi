from dataclasses import dataclass, field
from uuid import UUID

from shared.domain.utils import empty_uuid


@dataclass(frozen=True, kw_only=True)
class Entity:
    id: UUID = field(default_factory=empty_uuid)
    created_at: float = 0
    updated_at: float = 0
