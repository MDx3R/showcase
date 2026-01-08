"""Skill domain entity within course bounded context."""

from dataclasses import dataclass
from uuid import UUID

from common.domain.exceptions import InvariantViolationError


@dataclass
class Skill:
    """Skill entity for acquired skills in courses."""

    skill_id: UUID
    name: str
    description: str | None

    def __post_init__(self) -> None:
        """Validate domain invariants."""
        if not self.name or not self.name.strip():
            raise InvariantViolationError("Skill name cannot be empty")
