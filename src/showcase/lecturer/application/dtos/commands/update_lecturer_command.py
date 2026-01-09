"""Command DTO for UpdateLecturer (application layer - frozen dataclass)."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UpdateLecturerCommand:
    lecturer_id: UUID
    name: str
    position: str | None
    bio: str | None
    photo_url: str | None
    competencies: list[str]
