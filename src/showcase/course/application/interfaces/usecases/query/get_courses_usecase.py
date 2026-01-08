"""Get courses use case interface."""

from abc import ABC, abstractmethod

from showcase.course.application.dtos.queries import GetCoursesQuery
from showcase.course.application.read_models.course_read_model import CourseReadModel


class IGetCoursesUseCase(ABC):
    """Interface for getting courses."""

    @abstractmethod
    async def execute(self, query: GetCoursesQuery) -> list[CourseReadModel]:
        """Execute the get courses query."""
        pass
