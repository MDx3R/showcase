"""DTO for CreateSkill command."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateSkillCommand:
    name: str
    description: str | None = None
