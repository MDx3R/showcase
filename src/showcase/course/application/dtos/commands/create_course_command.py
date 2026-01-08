"""DTO for CreateCourse command."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field
from showcase.course.domain.value_objects import (
    CertificateType,
    CourseStatus,
    EducationFormat,
    Format,
)


class CreateCourseSectionDTO(BaseModel):
    """DTO for creating a course section."""

    name: str
    description: str | None
    order_num: int = Field(default=0, ge=0)
    hours: int | None = Field(default=None, ge=1)


class CreateCourseCommand(BaseModel):
    name: str
    description: str | None

    format: Format
    education_format: EducationFormat
    certificate_type: CertificateType

    cost: Decimal
    discounted_cost: Decimal | None
    duration_hours: int = Field(default=0, ge=0)

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
