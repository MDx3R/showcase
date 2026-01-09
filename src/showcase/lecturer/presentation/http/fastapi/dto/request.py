"""Presentation layer request DTOs for lecturer with validation."""

from pydantic import BaseModel, Field


class CreateLecturerRequest(BaseModel):
    """Request model for creating a lecturer."""

    name: str = Field(min_length=1, max_length=255)
    position: str | None = None
    bio: str | None = None
    photo_url: str | None = None
    competencies: list[str] = Field(default_factory=list)


class UpdateLecturerRequest(BaseModel):
    """Request model for updating a lecturer (without lecturer_id in body)."""

    name: str = Field(..., min_length=1, max_length=255)
    position: str | None
    bio: str | None
    photo_url: str | None
    competencies: list[str]
