"""DTO for CreateLecturer command."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateLecturerCommand:
    name: str
    position: str | None = None
    bio: str | None = None
    photo_url: str | None = None
