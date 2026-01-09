"""Presentation layer request DTOs with validation."""

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


# ============ Course Request Models ============
class CreateCourseSectionRequest(BaseModel):
    """Request model for creating a course section."""

    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    order_num: int = Field(ge=0)
    hours: int | None = Field(default=None, ge=1)


class CreateCourseRequest(BaseModel):
    """Request model for creating a course (without course_id)."""

    name: str = Field(min_length=1, max_length=255)
    description: str | None
    format: Format
    education_format: EducationFormat
    certificate_type: CertificateType
    cost: Decimal = Field(ge=0)
    discounted_cost: Decimal | None = Field(..., ge=0)
    duration_hours: int = Field(gt=0)
    start_date: datetime | None
    end_date: datetime | None
    status: CourseStatus
    is_published: bool
    locations: list[str] = Field(default_factory=list[str])
    sections: list[CreateCourseSectionRequest] = Field(
        default_factory=list[CreateCourseSectionRequest]
    )
    tags: list[str] = Field(default_factory=list[str])
    acquired_skill_ids: list[UUID] = Field(default_factory=list[UUID])
    category_ids: list[UUID] = Field(default_factory=list[UUID])
    lecturer_ids: list[UUID] = Field(default_factory=list[UUID])


class UpdateCourseSectionRequest(BaseModel):
    """Request model for updating a course section."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None
    order_num: int = Field(..., ge=0)
    hours: int | None = Field(..., ge=1)


class UpdateCourseRequest(BaseModel):
    """Request model for updating a course (without course_id in body)."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None
    format: Format
    education_format: EducationFormat
    certificate_type: CertificateType
    cost: Decimal = Field(..., ge=0)
    discounted_cost: Decimal = Field(..., ge=0)
    duration_hours: int = Field(..., gt=0)
    start_date: datetime | None  # ISO format
    end_date: datetime | None  # ISO format
    status: CourseStatus
    is_published: bool
    locations: list[str] = Field(default_factory=list[str])
    sections: list[CreateCourseSectionRequest] = Field(
        default_factory=list[CreateCourseSectionRequest]
    )
    tags: list[str] = Field(default_factory=list[str])
    acquired_skill_ids: list[UUID] = Field(default_factory=list[UUID])
    category_ids: list[UUID] = Field(default_factory=list[UUID])
    lecturer_ids: list[UUID] = Field(default_factory=list[UUID])


# ============ Skill Request Models ============
class CreateSkillRequest(BaseModel):
    """Request model for creating a skill."""

    name: str = Field(min_length=1, max_length=255)
    description: str | None


class UpdateSkillRequest(BaseModel):
    """Request model for updating a skill (without skill_id in body)."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None


# ============ Tag Request Models ============
class CreateTagRequest(BaseModel):
    """Request model for creating a tag."""

    name: str = Field(min_length=1, max_length=255)


class UpdateTagRequest(BaseModel):
    """Request model for updating a tag (without tag_id in body)."""

    name: str = Field(min_length=1, max_length=255)


# ============ Enrollment Request Models ============
class EnrollRequest(BaseModel):
    """Request model for enrolling a user (unauthenticated)."""

    email: str = Field(min_length=1)
    full_name: str = Field(min_length=1, max_length=255)
    phone: str | None = None
    message: str | None = None


class EnrollAuthenticatedRequest(BaseModel):
    """Request model for enrolling an authenticated user."""

    full_name: str = Field(min_length=1, max_length=255)
    phone: str | None = None
    message: str | None = None
