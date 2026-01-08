"""Get course by ID query DTO."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetCourseByIdQuery:
    """Query to get a course by ID."""

    course_id: UUID
