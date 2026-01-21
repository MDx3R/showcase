from abc import ABC, abstractmethod

from showcase.course.application.read_models.course_read_model import CourseReadModel


class ICourseRankingService(ABC):
    """Ranks courses by relevance to user query."""

    @abstractmethod
    async def rank(
        self, query: str, courses: list[CourseReadModel]
    ) -> tuple[list[CourseReadModel], bool]:
        """Rank courses by relevance. Returns (ranked_courses, ranking_weak)."""
        ...
