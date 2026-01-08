"""Course domain entity."""

from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from common.domain.exceptions import InvariantViolationError
from common.domain.value_objects.datetime import DateTime
from showcase.course.domain.value_objects import CertificateType, CourseStatus, Format
from showcase.course.domain.value_objects.format import EducationFormat


@dataclass(frozen=True)
class CourseSection:
    """A section (module) within a course - value object of Course aggregate."""

    # section_id: UUID # remove from domain, refactor behaviour from entity to vo; thus leave field on persistence side for record identity, set database defaults
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
    education_format: EducationFormat  # new
    duration_hours: int
    cost: Decimal
    discounted_cost: Decimal | None
    certificate_type: CertificateType

    start_date: DateTime | None  # type change from datetime; use timezone aware only vo
    end_date: DateTime | None  # new

    status: CourseStatus
    is_published: bool

    locations: list[str] = field(default_factory=list[str])  # new

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
            orders = {s.order_num for s in self.sections}
            if len(self.sections) != len(orders):
                raise InvariantViolationError("Section order numbers must be unique")
