"""Get lecturer by ID query DTO."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetLecturerByIdQuery:
    """Query to get a lecturer by ID."""

    lecturer_id: UUID
