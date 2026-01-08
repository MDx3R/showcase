"""Course read models."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from showcase.category.application.read_models.category_read_model import (
    CategoryReadModel,
)
from showcase.course.application.read_models.skill_read_model import SkillReadModel
from showcase.course.domain.value_objects import (
    CertificateType,
    CourseStatus,
    EducationFormat,
    Format,
)
from showcase.lecturer.application.read_models.lecturer_read_model import (
    LecturerReadModel,
)


@dataclass(frozen=True)
class CourseSectionReadModel:
    """Immutable read model for course section."""

    section_id: UUID
    name: str
    description: str | None
    order_num: int
    hours: int | None


class CourseReadModel(BaseModel):
    """Immutable read model for course with enriched nested objects."""

    course_id: UUID
    name: str
    description: str | None
    format: Format
    education_format: EducationFormat
    duration_hours: int
    cost: Decimal
    discounted_cost: Decimal | None
    start_date: datetime | None
    end_date: datetime | None
    certificate_type: CertificateType
    status: CourseStatus
    is_published: bool
    locations: list[str]
    categories: list[CategoryReadModel]
    tags: list[str]
    acquired_skills: list[SkillReadModel]
    lecturers: list[LecturerReadModel]
    sections: list[CourseSectionReadModel]
    created_at: datetime
    updated_at: datetime
