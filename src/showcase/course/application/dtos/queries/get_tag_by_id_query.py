"""DTO for GetTagById query."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetTagByIdQuery:
    tag_id: UUID
