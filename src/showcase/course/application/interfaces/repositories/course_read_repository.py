"""Course read repository interface."""

from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel
from showcase.course.application.read_models.course_read_model import CourseReadModel
from showcase.course.domain.value_objects import CourseStatus
from showcase.course.domain.value_objects.format import Format


class CourseFilter(BaseModel):
    categories: list[str] | None = None
    format: Format | None = None
    max_duration_hours: int | None = None
    certificate_required: bool | None = None
    status: CourseStatus = CourseStatus.ACTIVE
    is_published: bool = True
    limit: int = 10
    skip: int = 0


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
    async def filter(self, filter: CourseFilter) -> list[CourseReadModel]:
        """Deterministic filtering.

        Returns top-N courses strictly matching filters.
        """
        pass
