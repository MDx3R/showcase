"""DTO for UpdateCourse command."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field
from showcase.course.domain.value_objects import CertificateType, CourseStatus, Format


class UpdateCourseSectionDTO(BaseModel):
    """DTO for updating a course section."""

    section_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    order_num: int | None = Field(default=None, ge=0)
    hours: int | None = Field(default=None, ge=1)


class UpdateCourseCommand(BaseModel):
    course_id: UUID
    name: str | None = None
    description: str | None = None
    format: Format | None = None
    duration_hours: int | None = Field(default=None, ge=0)
    cost: Decimal | None = None
    discounted_cost: Decimal | None = None
    start_date: datetime | None = None
    certificate_type: CertificateType | None = None
    status: CourseStatus | None = None
    is_published: bool | None = None
    sections: list[UpdateCourseSectionDTO] | None = None

    tags: list[str] | None = None
    acquired_skill_ids: list[UUID] | None = None

    category_ids: list[UUID] | None = None
    lecturer_ids: list[UUID] | None = None
