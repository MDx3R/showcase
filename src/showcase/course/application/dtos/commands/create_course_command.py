"""DTO for CreateCourse command."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field
from showcase.course.domain.value_objects import CertificateType, CourseStatus, Format


class CreateCourseSectionDTO(BaseModel):
    """DTO for creating a course section."""

    name: str
    description: str | None = None
    order_num: int = Field(default=0, ge=0)
    hours: int | None = Field(default=None, ge=1)


class CreateCourseCommand(BaseModel):
    name: str
    description: str | None = None
    format: Format = Format.ONLINE
    duration_hours: int = Field(default=0, ge=0)
    cost: Decimal = Decimal("0.00")
    discounted_cost: Decimal | None = None
    start_date: datetime | None = None
    certificate_type: CertificateType = CertificateType.CERTIFICATE
    status: CourseStatus = CourseStatus.DRAFT
    is_published: bool = False
    sections: list[CreateCourseSectionDTO] | None = None

    tags: list[str] | None = None
    acquired_skill_ids: list[UUID] | None = None

    category_ids: list[UUID] | None = None
    lecturer_ids: list[UUID] | None = None
