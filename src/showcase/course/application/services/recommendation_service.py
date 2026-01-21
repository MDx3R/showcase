"""Recommendation orchestrator: coordinates filter inference, retrieval, and ranking."""

import logging

from showcase.category.application.interfaces.repositories.category_read_repository import (
    ICategoryReadRepository,
)
from showcase.course.application.interfaces.services.course_ranking_service import (
    ICourseRankingService,
)
from showcase.course.application.interfaces.services.course_retrieval_service import (
    ICourseRetrievalService,
)
from showcase.course.application.interfaces.services.filter_inference_service import (
    IFilterInferenceService,
)
from showcase.course.application.interfaces.services.recommendation_service import (
    GetRecommendationsDTO,
    IRecommendationService,
    RecommendationNotice,
    RecommendationsDTO,
)


class RecommendationService(IRecommendationService):
    """Orchestrates filter inference, course retrieval, and LLM ranking."""

    MAX_LIMIT: int = 25
    FALLBACK_RANKING_QUERY = """
        Предложи курсы, отсортированные по предполагаемой востребованности для широкой аудитории.

        Критерии:
        - универсальность
        - актуальность
        - прикладная ценность
        - не нишевость
    """

    def __init__(
        self,
        logger: logging.Logger,
        category_repository: ICategoryReadRepository,
        filter_inference: IFilterInferenceService,
        course_retrieval: ICourseRetrievalService,
        course_ranking: ICourseRankingService,
    ) -> None:
        self._logger = logger
        self._category_repository = category_repository
        self._filter_inference = filter_inference
        self._course_retrieval = course_retrieval
        self._course_ranking = course_ranking

    async def recommend(self, dto: GetRecommendationsDTO) -> RecommendationsDTO:
        query = dto.query
        notices: list[RecommendationNotice] = []

        self._logger.info(
            "Recommendation started",
            extra={
                "action": "recommend",
                "query": query[:200],
                "limit": dto.limit,
                "skip": dto.skip,
            },
        )

        # 1. Load categories
        categories = await self._category_repository.get_all()
        category_names = {c.name for c in categories}
        self._logger.debug(
            "Categories loaded",
            extra={"action": "recommend", "count": len(categories)},
        )

        # 2. Infer filter from query
        filter_llm = await self._filter_inference.infer(query, category_names)

        # 3. Retrieve courses: by filter or fallback
        limit = min(self.MAX_LIMIT, dto.limit)
        courses = await self._course_retrieval.filter_by_inference(
            filter_llm, category_names, limit=limit, skip=dto.skip
        )

        if courses:
            notices.append(RecommendationNotice.FILTERS_INFERRED)

        if not courses:
            query = self.FALLBACK_RANKING_QUERY
            notices.append(
                RecommendationNotice.QUERY_INVALID
                if not filter_llm.is_decisive
                else RecommendationNotice.QUERY_AMBIGUOUS
            )
            notices.append(RecommendationNotice.FALLBACK_USED)

            courses = await self._course_retrieval.get_fallback_courses(
                limit=self.MAX_LIMIT
            )

            self._logger.info(
                "Fallback applied",
                extra={
                    "action": "recommend",
                    "reason": (
                        "indecisive" if not filter_llm.is_decisive else "no_courses"
                    ),
                    "fallback_count": len(courses),
                },
            )

        # 4. Rank by LLM
        ranked, ranking_weak = await self._course_ranking.rank(query, courses)
        if ranking_weak:
            notices.append(RecommendationNotice.RANKING_WEAK)

        # 5. Build result
        result_courses = ranked[:limit]
        result = RecommendationsDTO(
            notices=notices, courses=result_courses, skip=dto.skip + len(ranked)
        )

        self._logger.info(
            "Recommendation completed",
            extra={
                "action": "recommend",
                "courses_count": len(result_courses),
                "notices": notices,
                "skip": result.skip,
            },
        )

        return result
