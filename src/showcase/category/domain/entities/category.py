"""Category domain entity."""

from dataclasses import dataclass
from uuid import UUID

from common.domain.exceptions import InvariantViolationError


@dataclass
class Category:
    """Category entity for course classification."""

    category_id: UUID
    name: str
    description: str | None

    def __post_init__(self) -> None:
        """Validate domain invariants."""
        if not self.name or not self.name.strip():
            raise InvariantViolationError("Category name cannot be empty")
