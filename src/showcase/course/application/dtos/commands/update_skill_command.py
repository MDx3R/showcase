"""DTO for UpdateSkill command."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateSkillCommand:
    skill_id: UUID
    name: str | None = None
    description: str | None = None
