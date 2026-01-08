"""DTO for UpdateSkill command."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateSkillCommand:
    skill_id: UUID
    name: str
    description: str | None
