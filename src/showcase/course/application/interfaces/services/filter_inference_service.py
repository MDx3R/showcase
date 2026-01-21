from abc import ABC, abstractmethod

from showcase.course.application.read_models.filter_inference import CourseFilterLLM


class IFilterInferenceService(ABC):
    """Infers structured course filter from user query."""

    @abstractmethod
    async def infer(self, query: str, category_names: set[str]) -> CourseFilterLLM:
        """Infer CourseFilterLLM from user query and available categories."""
        ...
