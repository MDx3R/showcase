"""Use case: search courses by full-text query."""

from abc import ABC, abstractmethod

from showcase.course.application.dtos.queries.get_courses_search_query import (
    GetCoursesSearchQuery,
)
from showcase.course.application.read_models.course_read_model import CourseReadModel


class IGetCoursesSearchUseCase(ABC):
    @abstractmethod
    async def execute(self, query: GetCoursesSearchQuery) -> list[CourseReadModel]: ...
