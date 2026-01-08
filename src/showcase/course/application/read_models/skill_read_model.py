"""Skill read model within course bounded context."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SkillReadModel:
    """Immutable read model for skill."""

    skill_id: UUID
    name: str
    description: str | None
