from abc import ABC, abstractmethod

from showcase.course.application.read_models.course_read_model import CourseReadModel
from showcase.course.application.read_models.filter_inference import CourseFilterLLM


class ICourseRetrievalService(ABC):
    """Fetches courses by inferred filter or provides fallback list."""

    @abstractmethod
    async def filter_by_inference(
        self,
        filter_llm: CourseFilterLLM,
        available_category_names: set[str],
        limit: int,
        skip: int,
    ) -> list[CourseReadModel]:
        """Apply inferred filter and return courses. Empty list if indecisive or no params."""
        ...

    @abstractmethod
    async def get_fallback_courses(self, limit: int) -> list[CourseReadModel]:
        """Return courses for fallback path: get_all + shuffle."""
        ...
