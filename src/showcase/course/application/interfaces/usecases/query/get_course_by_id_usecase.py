"""Get course by ID use case interface."""

from abc import ABC, abstractmethod

from showcase.course.application.dtos.queries import GetCourseByIdQuery
from showcase.course.application.read_models.course_read_model import CourseReadModel


class IGetCourseByIdUseCase(ABC):
    """Interface for getting a course by ID."""

    @abstractmethod
    async def execute(self, query: GetCourseByIdQuery) -> CourseReadModel:
        """Execute the get course by ID query."""
        pass
