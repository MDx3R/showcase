"""DTO for UpdateLecturer command."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateLecturerCommand:
    lecturer_id: UUID
    name: str | None = None
    position: str | None = None
    bio: str | None = None
    photo_url: str | None = None
