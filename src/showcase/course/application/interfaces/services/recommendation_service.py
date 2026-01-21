from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from showcase.course.application.read_models.course_read_model import CourseReadModel


class RecommendationNotice(str, Enum):
    QUERY_INVALID = "query_invalid"
    QUERY_AMBIGUOUS = "query_ambiguous"
    FALLBACK_USED = "fallback_used"
    RANKING_WEAK = "ranking_weak"
    FILTERS_INFERRED = "filters_inferred"


@dataclass(frozen=True)
class GetRecommendationsDTO:
    query: str
    limit: int = 10
    skip: int = 0


@dataclass(frozen=True)
class RecommendationsDTO:
    notices: list[RecommendationNotice]
    courses: list[CourseReadModel]
    skip: int


class IRecommendationService(ABC):
    @abstractmethod
    async def recommend(self, dto: GetRecommendationsDTO) -> RecommendationsDTO: ...
