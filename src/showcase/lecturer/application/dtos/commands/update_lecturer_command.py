"""DTO for UpdateLecturer command."""

from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class UpdateLecturerCommand:
    lecturer_id: UUID
    name: str
    position: str | None
    bio: str | None
    photo_url: str | None
    competencies: list[str] = field(default_factory=list[str])
