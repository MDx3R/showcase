"""Command DTO for UpdateTag (application layer - frozen dataclass)."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateTagCommand:
    tag_id: UUID
    name: str
