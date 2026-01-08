"""Category read models."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class CategoryReadModel:
    """Immutable read model for category."""

    category_id: UUID
    name: str
    description: str | None
