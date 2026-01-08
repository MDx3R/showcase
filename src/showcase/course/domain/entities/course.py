"""Course domain entity."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from common.domain.exceptions import InvariantViolationError
from showcase.course.domain.value_objects import CertificateType, CourseStatus, Format


@dataclass
class CourseSection:
    """A section (module) within a course - value object of Course aggregate."""

    section_id: UUID
    name: str
    description: str | None
    order_num: int
    hours: int | None

    def __post_init__(self) -> None:
        """Validate section invariants."""
        if not self.name or not self.name.strip():
            raise InvariantViolationError("Section name cannot be empty")
        if self.order_num < 0:
            raise InvariantViolationError("Section order must be non-negative")
        if self.hours is not None and self.hours < 0:
            raise InvariantViolationError("Section hours cannot be negative")


@dataclass
class Course:
    """Course aggregate root with sections as part of the aggregate."""

    course_id: UUID
    name: str
    description: str | None
    format: Format
    duration_hours: int
    cost: Decimal
    discounted_cost: Decimal | None
    start_date: datetime | None
    certificate_type: CertificateType
    status: CourseStatus
    is_published: bool

    sections: list[CourseSection] = field(default_factory=list[CourseSection])

    tag_ids: list[UUID] = field(default_factory=list[UUID])
    acquired_skill_ids: list[UUID] = field(default_factory=list[UUID])

    category_ids: list[UUID] = field(default_factory=list[UUID])
    lecturer_ids: list[UUID] = field(default_factory=list[UUID])

    def __post_init__(self) -> None:
        """Validate aggregate invariants."""
        if not self.name or not self.name.strip():
            raise InvariantViolationError("Course name cannot be empty")
        if self.duration_hours <= 0:
            raise InvariantViolationError("Course duration must be positive")
        if self.cost < 0:
            raise InvariantViolationError("Course cost cannot be negative")
        if self.discounted_cost is not None:
            if self.discounted_cost < 0:
                raise InvariantViolationError("Discounted cost cannot be negative")
            if self.discounted_cost > self.cost:
                raise InvariantViolationError("Discounted cost cannot exceed cost")
        if self.is_published and self.status == CourseStatus.DRAFT:
            raise InvariantViolationError("Published course cannot have DRAFT status")
        # Validate section ordering is unique and sequential
        if self.sections:
            orders = sorted([s.order_num for s in self.sections])
            if len(orders) != len(set(orders)):
                raise InvariantViolationError("Section order numbers must be unique")

    def add_section(self, section: CourseSection) -> None:
        """Add a section to the course."""
        if any(s.order_num == section.order_num for s in self.sections):
            raise InvariantViolationError(
                f"Section with order {section.order_num} already exists"
            )
        self.sections.append(section)

    def remove_section(self, section_id: UUID) -> None:
        """Remove a section from the course."""
        self.sections = [s for s in self.sections if s.section_id != section_id]

    def update_section(self, section: CourseSection) -> None:
        """Update an existing section."""
        for i, s in enumerate(self.sections):
            if s.section_id == section.section_id:
                self.sections[i] = section
                return
        raise InvariantViolationError(f"Section {section.section_id} not found")
