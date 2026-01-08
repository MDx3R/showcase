"""Lecturer domain entity."""

from dataclasses import dataclass
from uuid import UUID

from common.domain.exceptions import InvariantViolationError


@dataclass
class Lecturer:
    """Lecturer entity."""

    lecturer_id: UUID
    name: str
    position: str | None
    bio: str | None
    photo_url: str | None

    def __post_init__(self) -> None:
        """Validate domain invariants."""
        if not self.name or not self.name.strip():
            raise InvariantViolationError("Lecturer name cannot be empty")
