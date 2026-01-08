"""Lecturer domain entity."""

from dataclasses import dataclass, field
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
    competencies: list[str] = field(default_factory=list[str])

    def __post_init__(self) -> None:
        """Validate domain invariants."""
        if not self.name or not self.name.strip():
            raise InvariantViolationError("Lecturer name cannot be empty")
