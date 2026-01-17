"""Course read repository interface."""

from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID

from pydantic import BaseModel
from showcase.course.application.read_models.course_read_model import CourseReadModel
from showcase.course.domain.value_objects import CourseStatus
from showcase.course.domain.value_objects.format import EducationFormat, Format


class CourseSortField(str, Enum):
    TITLE = "title"
    PRICE = "price"
    DURATION = "duration"
    NONE = "none"


class CourseSortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SimpleCoursesFilter(BaseModel):
    """Simplified filter to get all courses with optional filters."""

    status: CourseStatus = CourseStatus.ACTIVE
    is_published: bool = True

    categories: list[str] | None = None
    format: Format | None = None
    max_duration_hours: int | None = None
    certificate_required: bool | None = None

    skip: int = 0
    limit: int = 10


class CoursesFilter(BaseModel):
    """Filter to get all courses with optional filters."""

    # base filters
    is_published: bool | None = None
    status: CourseStatus | None = None

    # text search
    search: str | None = None

    # taxonomy filters
    formats: list[Format] | None = None
    education_types: list[EducationFormat] | None = None

    tags: list[str] | None = None
    category_ids: list[UUID] | None = None

    # price filters
    price_min: int | None = None
    price_max: int | None = None

    # duration filters (e.g. hours / weeks — на уровне сервиса)
    duration_min: int | None = None
    duration_max: int | None = None

    # flags
    has_discount: bool | None = None
    is_upcoming: bool | None = None

    # sorting
    sort_field: CourseSortField = CourseSortField.NONE
    sort_order: CourseSortOrder = CourseSortOrder.ASC

    # pagination
    skip: int = 0
    limit: int = 100


class ICourseReadRepository(ABC):
    """Interface for reading courses."""

    @abstractmethod
    async def get_by_id(self, course_id: UUID) -> CourseReadModel:
        """Get a course by ID."""
        pass

    @abstractmethod
    async def get_all(
        self,
        status: CourseStatus | None = None,
        is_published: bool | None = None,
        category_id: UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[CourseReadModel]:
        """Get all courses with optional filters."""
        pass

    @abstractmethod
    async def search(
        self, query: str, skip: int = 0, limit: int = 50
    ) -> list[CourseReadModel]:
        """Full-text search courses by query string."""
        pass

    @abstractmethod
    async def filter(self, filter: SimpleCoursesFilter) -> list[CourseReadModel]:
        """Deterministic simple filtering.

        Returns top-N courses strictly matching filters.
        """
        pass

    @abstractmethod
    async def filter_extended(self, filter: CoursesFilter) -> list[CourseReadModel]:
        """Deterministic extended filtering."""
        pass
