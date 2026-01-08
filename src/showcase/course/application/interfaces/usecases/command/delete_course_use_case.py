"""Use case interface for deleting a course."""

from abc import ABC, abstractmethod
from uuid import UUID


class IDeleteCourseUseCase(ABC):
    """Interface for deleting a course."""

    @abstractmethod
    async def execute(self, course_id: UUID) -> UUID:
        """Execute the use case."""
        pass
