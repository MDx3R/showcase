"""Command DTO for UpdateCourse (application layer - frozen dataclass)."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from showcase.course.domain.value_objects import (
    CertificateType,
    CourseStatus,
    Format,
)
from showcase.course.domain.value_objects.format import EducationFormat


@dataclass(frozen=True)
class UpdateCourseSectionDTO:
    """DTO for updating a course section."""

    name: str
    description: str | None
    order_num: int
    hours: int | None


@dataclass(frozen=True)
class UpdateCourseCommand:
    """Command to update a course."""

    course_id: UUID
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

    sections: list[UpdateCourseSectionDTO]

    tags: list[str]
    acquired_skill_ids: list[UUID]

    category_ids: list[UUID]
    lecturer_ids: list[UUID]
