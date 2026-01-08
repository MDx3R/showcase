"""SQLAlchemy models for Course, sections, and associations."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID, uuid4

from common.domain.value_objects.datetime import DateTime
from common.infrastructure.database.postgres.sqlalchemy.models import Base
from showcase.category.infrastructure.database.postgres.sqlalchemy.models import (
    CategoryBase,
)
from showcase.course.domain.value_objects import (
    CertificateType,
    CourseStatus,
    EducationFormat,
    Format,
)
from showcase.course.infrastructure.database.postgres.sqlalchemy.models.skill import (
    SkillBase,
)
from showcase.course.infrastructure.database.postgres.sqlalchemy.models.tag import (
    TagBase,
)
from showcase.lecturer.infrastructure.database.postgres.sqlalchemy.models import (
    LecturerBase,
)
from sqlalchemy import (
    Boolean,
    DateTime as SQLDateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CourseBase(Base):
    """SQLAlchemy model for Course."""

    __tablename__ = "courses"

    course_id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    format: Mapped[Format] = mapped_column(Enum(Format), nullable=False)
    education_format: Mapped[EducationFormat] = mapped_column(
        Enum(EducationFormat), nullable=False
    )
    duration_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    discounted_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    start_date: Mapped[DateTime | None] = mapped_column(
        SQLDateTime(timezone=True), nullable=True
    )
    end_date: Mapped[DateTime | None] = mapped_column(
        SQLDateTime(timezone=True), nullable=True
    )
    certificate_type: Mapped[CertificateType] = mapped_column(
        Enum(CertificateType), nullable=False
    )
    status: Mapped[CourseStatus] = mapped_column(
        Enum(CourseStatus), nullable=False, default=CourseStatus.DRAFT
    )
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    locations: Mapped[list[str]] = mapped_column(
        ARRAY(String(255)), nullable=False, server_default=text("'{}'")
    )

    sections: Mapped[list[CourseSectionBase]] = relationship(
        "CourseSectionBase", lazy="noload", order_by="CourseSectionBase.order_num"
    )

    categories: Mapped[list[CategoryBase]] = relationship(
        "CategoryBase",
        secondary="course_categories",
        lazy="noload",
        passive_deletes=True,
    )
    tags: Mapped[list[TagBase]] = relationship(
        "TagBase", secondary="course_tags", lazy="noload", passive_deletes=True
    )
    acquired_skills: Mapped[list[SkillBase]] = relationship(
        "SkillBase", secondary="course_skills", lazy="noload", passive_deletes=True
    )
    lecturers: Mapped[list[LecturerBase]] = relationship(
        "LecturerBase",
        secondary="course_lecturers",
        lazy="noload",
        passive_deletes=True,
    )


class CourseSectionBase(Base):
    """SQLAlchemy model for Course Section."""

    __tablename__ = "course_sections"

    section_id: Mapped[UUID] = mapped_column(PGUUID, primary_key=True, default=uuid4)
    course_id: Mapped[UUID] = mapped_column(
        ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    order_num: Mapped[int] = mapped_column(Integer, nullable=False)
    hours: Mapped[int | None] = mapped_column(Integer)


class CourseCategoryBase(Base):
    """SQLAlchemy model for Course-Category association."""

    __tablename__ = "course_categories"

    course_id: Mapped[UUID] = mapped_column(
        ForeignKey("courses.course_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.category_id"), nullable=False, primary_key=True
    )


class CourseTagBase(Base):
    """SQLAlchemy model for Course-Tag association."""

    __tablename__ = "course_tags"

    course_id: Mapped[UUID] = mapped_column(
        ForeignKey("courses.course_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    tag_id: Mapped[UUID] = mapped_column(
        ForeignKey("tags.tag_id"), nullable=False, primary_key=True
    )


class CourseSkillBase(Base):
    """SQLAlchemy model for Course-Skill association."""

    __tablename__ = "course_skills"

    course_id: Mapped[UUID] = mapped_column(
        ForeignKey("courses.course_id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    skill_id: Mapped[UUID] = mapped_column(
        ForeignKey("skills.skill_id"), nullable=False, primary_key=True
    )


class CourseLecturerBase(Base):
    """SQLAlchemy model for Course-Lecturer association."""

    __tablename__ = "course_lecturers"

    course_id: Mapped[UUID] = mapped_column(
        ForeignKey("courses.course_id"), nullable=False, primary_key=True
    )
    lecturer_id: Mapped[UUID] = mapped_column(
        ForeignKey("lecturers.lecturer_id"), nullable=False, primary_key=True
    )
