"""Get courses query DTO."""

from dataclasses import dataclass
from uuid import UUID

from showcase.course.domain.value_objects import CourseStatus, Format


@dataclass
class GetCoursesQuery:
    """Query to get all courses with optional filters."""

    status: CourseStatus | None = None
    is_published: bool | None = None
    category_id: UUID | None = None
    format: Format | None = None
    skip: int = 0
    limit: int = 100
