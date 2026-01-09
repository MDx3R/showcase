"""Command DTO for UpdateCategory (application layer - frozen dataclass)."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateCategoryCommand:
    category_id: UUID
    name: str
    description: str | None
