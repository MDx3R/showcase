from abc import ABC, abstractmethod
from dataclasses import dataclass

from showcase.course.application.read_models.course_read_model import CourseReadModel


@dataclass(frozen=True)
class GetRecommendationsDTO:
    query: str
    limit: int = 10
    skip: int = 0


@dataclass(frozen=True)
class RecommendationsDTO:
    courses: list[CourseReadModel]
    skip: int


class IRecommendationService(ABC):
    @abstractmethod
    async def recommend(self, dto: GetRecommendationsDTO) -> RecommendationsDTO: ...
