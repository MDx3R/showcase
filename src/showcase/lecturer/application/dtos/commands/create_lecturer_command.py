"""DTO for CreateLecturer command."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CreateLecturerCommand:
    name: str
    position: str | None
    bio: str | None
    photo_url: str | None
    competencies: list[str] = field(default_factory=list[str])
