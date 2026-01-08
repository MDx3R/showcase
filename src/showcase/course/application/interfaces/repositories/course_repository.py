"""Write repository interface for courses."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.course.domain.entities.course import Course


class ICourseRepository(ABC):
    """Interface for writing courses."""

    @abstractmethod
    async def get_by_id(self, course_id: UUID) -> Course:
        """Get a course by ID."""
        pass

    @abstractmethod
    async def add(self, course: Course) -> None:
        """Add a new course."""
        pass

    @abstractmethod
    async def update(self, course: Course) -> None:
        """Update an existing course."""
        pass

    @abstractmethod
    async def delete(self, course_id: UUID) -> None:
        """Delete a course by ID."""
        pass
