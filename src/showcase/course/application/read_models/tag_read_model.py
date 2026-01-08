"""Tag read model."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class TagReadModel:
    """Immutable read model for tag."""

    tag_id: UUID
    value: str
