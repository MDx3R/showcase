"""Lecturer read models."""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class LecturerReadModel:
    """Immutable read model for lecturer."""

    lecturer_id: UUID
    name: str
    position: str | None
    bio: str | None
    photo_url: str | None
    competencies: list[str]
