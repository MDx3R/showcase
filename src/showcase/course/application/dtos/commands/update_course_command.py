"""DTO for UpdateCourse command."""

from decimal import Decimal
from uuid import UUID

from common.domain.value_objects.datetime import DateTime
from pydantic import BaseModel, Field
from showcase.course.domain.value_objects import (
    CertificateType,
    CourseStatus,
    Format,
)
from showcase.course.domain.value_objects.format import EducationFormat


class UpdateCourseSectionDTO(BaseModel):
    """DTO for updating a course section."""

    name: str
    description: str | None
    order_num: int = Field(default=0, ge=0)
    hours: int | None = Field(default=None, ge=1)


class UpdateCourseCommand(BaseModel):
    course_id: UUID
    name: str
    description: str | None

    format: Format
    education_format: EducationFormat
    certificate_type: CertificateType

    cost: Decimal
    discounted_cost: Decimal | None
    duration_hours: int = Field(default=0, ge=0)

    start_date: DateTime | None
    end_date: DateTime | None

    status: CourseStatus
    is_published: bool

    locations: list[str]

    sections: list[UpdateCourseSectionDTO]

    tags: list[str]
    acquired_skill_ids: list[UUID]

    category_ids: list[UUID]
    lecturer_ids: list[UUID]
