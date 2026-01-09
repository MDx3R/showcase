"""Command DTO for CreateCourse (application layer - frozen dataclass)."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from showcase.course.domain.value_objects import (
    CertificateType,
    CourseStatus,
    EducationFormat,
    Format,
)


@dataclass(frozen=True)
class CreateCourseSectionDTO:
    """Value object for course section in command."""

    name: str
    description: str | None
    order_num: int
    hours: int | None


@dataclass(frozen=True)
class CreateCourseCommand:
    """Command to create a course."""

    name: str
    description: str | None

    format: Format
    education_format: EducationFormat
    certificate_type: CertificateType

    cost: Decimal
    discounted_cost: Decimal | None
    duration_hours: int
    start_date: datetime | None
    end_date: datetime | None

    status: CourseStatus
    is_published: bool

    locations: list[str]

    sections: list[CreateCourseSectionDTO]

    tags: list[str]
    acquired_skill_ids: list[UUID]

    category_ids: list[UUID]
    lecturer_ids: list[UUID]
