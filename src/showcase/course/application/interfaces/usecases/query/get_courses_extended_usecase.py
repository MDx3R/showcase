"""Interface for extended course filtering use case."""

from abc import ABC, abstractmethod

from showcase.course.application.interfaces.repositories.course_read_repository import (
    CoursesFilter,
)
from showcase.course.application.read_models.course_read_model import CourseReadModel


class IGetCoursesExtendedUseCase(ABC):
    @abstractmethod
    async def execute(self, query: CoursesFilter) -> list[CourseReadModel]: ...
