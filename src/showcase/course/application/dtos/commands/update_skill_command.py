"""Command DTO for UpdateSkill (application layer - frozen dataclass)."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateSkillCommand:
    skill_id: UUID
    name: str
    description: str | None
