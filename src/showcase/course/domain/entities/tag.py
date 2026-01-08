"""Tag domain entity."""

from dataclasses import dataclass
from uuid import UUID

from common.domain.exceptions import InvariantViolationError


@dataclass
class Tag:
    """Tag entity for course classification."""

    tag_id: UUID
    value: str

    def __post_init__(self) -> None:
        """Validate domain invariants."""
        if not self.value or not self.value.strip():
            raise InvariantViolationError("Tag name cannot be empty")
