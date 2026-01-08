"""DTO for UpdateCategory command."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateCategoryCommand:
    category_id: UUID
    name: str | None = None
    description: str | None = None
