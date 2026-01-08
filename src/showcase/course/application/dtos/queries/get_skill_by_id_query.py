"""DTO for GetSkillById query."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetSkillByIdQuery:
    skill_id: UUID
