"""DTO for GetSkills query."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GetSkillsQuery:
    skip: int = 0
    limit: int = 100
