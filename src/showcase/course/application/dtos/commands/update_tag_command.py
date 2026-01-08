"""DTO for UpdateTag command."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateTagCommand:
    tag_id: UUID
    name: str
