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


class CourseSectionRankingModel(BaseModel):
    """Optimized model for course section in ranking requests."""

    name: str
    description: str | None


class CourseRankingModel(BaseModel):
    """Optimized model for skill in ranking requests."""

    name: str
    description: str | None


class CourseRankingReadModel(BaseModel):
    """Optimized read model for LLM ranking requests.

    Contains only essential fields needed for ranking:
    - course_id: for identification
    - name: course title
    - description: course description
    - category_names: category names for relevance matching
    - skill_names: skill names for relevance matching
    - sections: section names and descriptions for content matching
    """

    course_id: UUID
    name: str
    description: str | None
    category_names: list[str]
    skill_names: list[CourseRankingModel]
    sections: list[CourseSectionRankingModel]

    @classmethod
    def from_course_read_model(
        cls, course: CourseReadModel
    ) -> "CourseRankingReadModel":
        """Convert CourseReadModel to optimized CourseRankingReadModel."""
        return cls(
            course_id=course.course_id,
            name=course.name,
            description=course.description,
            category_names=[cat.name for cat in course.categories],
            skill_names=[
                CourseRankingModel(name=skill.name, description=skill.description)
                for skill in course.acquired_skills
            ],
            sections=[
                CourseSectionRankingModel(
                    name=section.name,
                    description=section.description,
                )
                for section in course.sections
            ],
        )
