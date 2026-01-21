"""Course ranking: LLM-based ordering by relevance to user goal."""

import logging
from functools import reduce
from uuid import UUID

from llama_index.core import PromptTemplate
from llama_index.core.llms import LLM
from pydantic import BaseModel
from showcase.course.application.interfaces.services.course_ranking_service import (
    ICourseRankingService,
)
from showcase.course.application.read_models.course_read_model import (
    CourseRankingReadModel,
    CourseReadModel,
)


class CourseRankingItem(BaseModel):
    course_id: UUID
    confidence: float


class CourseRankingLLM(BaseModel):
    """Structured LLM response for course ranking."""

    courses: list[CourseRankingItem]


class CourseRankingService(ICourseRankingService):
    """Ranks courses by relevance to user query using LLM."""

    MIN_CONFIDENCE: float = 0.5
    RANKING_WEAK_THRESHOLD: int = 3
    RANKING_PROMPT = PromptTemplate(
        """
        Пользовательская цель:
        "{query}"

        Курсы:
        {courses}

        Верни JSON:
        - courses: list[{"course_id": UUID, "confidence": float}]

        Отсортируй курсы от наиболее подходящего к наименее подходящему, исключи полностью неподходящие.
        Курс должен быть ИСКЛЮЧЁН из списка, если:
        - у него нет категорий, связанных с целью
        - И нет навыков, связанных с целью
        - И описание курса или секций/модулей не содержит терминов, связанных с целью

        Отсутствие информации считается признаком неподходящего курса.
        Пример confidence:
        - 0.0 — совсем не подходит к цели пользователя
        - 0.25 — слабое совпадение, курс мало связан с запросом
        - 0.5 — умеренно релевантный курс, может быть полезен
        - 0.75 — хорошо подходит, совпадение заметное
        - 1.0 — идеально подходит, курс полностью соответствует цели
        """
    )

    def __init__(self, logger: logging.Logger, llm: LLM) -> None:
        self._logger = logger
        self._llm = llm

    async def rank(
        self, query: str, courses: list[CourseReadModel]
    ) -> tuple[list[CourseReadModel], bool]:
        """Rank courses by relevance. Returns (ranked_courses, ranking_weak).

        ranking_weak=True if LLM returned no/empty IDs → keep original order.
        """
        if not courses:
            self._logger.warning(
                "Ranking skipped: empty course list",
                extra={"service": "CourseRanking"},
            )
            return [], False

        ranking_courses = [
            CourseRankingReadModel.from_course_read_model(c) for c in courses
        ]
        courses_json = [c.model_dump(mode="json") for c in ranking_courses]

        self._logger.debug(
            "Sending ranking request to LLM",
            extra={
                "service": "CourseRanking",
                "query": query[:200],
                "courses_count": len(courses),
            },
        )

        ranking_llm = self._llm.as_structured_llm(CourseRankingLLM)
        formatted = self.RANKING_PROMPT.format(query=query, courses=courses_json)
        response = await ranking_llm.acomplete(formatted)
        result = CourseRankingLLM.model_validate_json(response.text)

        self._logger.info(
            "Ranking received",
            extra={
                "service": "CourseRanking",
                "ranked_count": len(result.courses),
                "ranked_ids": [str(c.course_id) for c in result.courses],
                "ranked_confidence": [c.confidence for c in result.courses],
            },
        )

        course_by_id = {c.course_id: c for c in courses}
        ranked = [
            course_by_id[c.course_id]
            for c in result.courses
            if c.course_id in course_by_id
        ]

        ranking_weak = not ranked

        if not ranked:
            self._logger.warning(
                "Ranking weak: no valid IDs, keeping original order",
                extra={"service": "CourseRanking", "input_count": len(courses)},
            )
            ranked = courses
            ranking_weak = True
        elif self.is_below_threshold(result.courses):
            self._logger.warning(
                "Ranking weak: confidence level is below threshold for all courses",
                extra={
                    "service": "CourseRanking",
                    "min_confidence": self.MIN_CONFIDENCE,
                    "ranked_confidence": [c.confidence for c in result.courses],
                },
            )
            ranking_weak = True

        return ranked, ranking_weak

    @classmethod
    def is_below_threshold(cls, courses: list[CourseRankingItem]) -> bool:
        if not courses:
            return True

        if len(courses) <= cls.RANKING_WEAK_THRESHOLD:
            return not any(c.confidence >= cls.MIN_CONFIDENCE for c in courses)

        return (
            reduce(
                lambda count, x: count + (x >= cls.MIN_CONFIDENCE),
                [c.confidence for c in courses],
                0,
            )
            <= cls.RANKING_WEAK_THRESHOLD
        )
