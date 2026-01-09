from uuid import UUID

from llama_index.core import PromptTemplate
from llama_index.core.llms import LLM
from pydantic import BaseModel
from showcase.category.application.interfaces.repositories.category_read_repository import (
    ICategoryReadRepository,
)
from showcase.course.application.interfaces.repositories.course_read_repository import (
    ICourseReadRepository,
    SimpleCoursesFilter,
)
from showcase.course.application.interfaces.services.recommendation_service import (
    GetRecommendationsDTO,
    IRecommendationService,
    RecommendationsDTO,
)
from showcase.course.domain.value_objects.format import Format


class CourseFilterLLM(BaseModel):
    category_names: list[str] | None = None
    format: Format | None = None
    max_duration_hours: int | None = None
    certificate_required: bool | None = None

    def to_filter(self, limit: int, skip: int) -> SimpleCoursesFilter:
        return SimpleCoursesFilter(
            categories=self.category_names,
            format=self.format,
            max_duration_hours=self.max_duration_hours,
            certificate_required=self.certificate_required,
            limit=limit,
            skip=skip,
        )


class CourseRankingLLM(BaseModel):
    course_ids: list[UUID]


class RecommendationService(IRecommendationService):
    MAX_LIMIT: int = 25

    def __init__(
        self,
        llm: LLM,
        course_repository: ICourseReadRepository,
        category_repository: ICategoryReadRepository,
    ) -> None:
        self.llm = llm
        self.course_repository = course_repository
        self.category_repository = category_repository

    async def recommend(self, dto: GetRecommendationsDTO) -> RecommendationsDTO:
        # ---------- 1. Categories ----------
        categories = await self.category_repository.get_all()
        category_names = {c.name.lower() for c in categories}

        # ---------- 2. LLM → SimpleCoursesFilter ----------
        filter_prompt = PromptTemplate(
            """
            Ты — ассистент подбора образовательных курсов.

            Запрос пользователя:
            "{query}"

            Доступные категории:
            {categories}

            Верни JSON с полями:
            - category_names: list[str] | null
            - format: "online" | "offline" | "mixed" | null
            - max_duration_hours: int | null
            - certificate_required: bool | null

            Если параметр не указан явно — верни null. 
            Разрешено использовать только доступные категории, если они есть. 
            Если категорий нет, верни null для category_names.
            """
        )

        filter_llm = self.llm.as_structured_llm(CourseFilterLLM)

        response = await filter_llm.acomplete(
            filter_prompt.format(
                query=dto.query, categories=", ".join(category_names) or "нет"
            )
        )

        filter_response = CourseFilterLLM.model_validate_json(response.text)

        # ---------- 3. Map LLM → SimpleCoursesFilter ----------
        filter_query = filter_response.to_filter(
            min(self.MAX_LIMIT, dto.limit), skip=dto.skip
        )

        # ---------- 4. DB filter ----------
        courses = await self.course_repository.filter(filter_query)

        if not courses:
            return RecommendationsDTO(courses=[], skip=dto.skip)

        # ---------- 5. LLM → Ranking ----------
        ranking_prompt = PromptTemplate(
            """
            Пользовательская цель:
            "{query}"

            Курсы:
            {courses}

            Верни JSON:
            - course_ids: list[UUID]

            Отсортируй курсы от наиболее подходящего к наименее подходящему, исключи полностью неподходящие.
            Курс должен быть ИСКЛЮЧЁН, если:
            - у него нет категорий, связанных с целью
            - И нет навыков, связанных с целью
            - И описание курса или секций/модулей не содержит терминов, связанных с целью

            Отсутствие информации считается признаком неподходящего курса.
            """
        )

        ranking_llm = self.llm.as_structured_llm(CourseRankingLLM)

        response = await ranking_llm.acomplete(
            ranking_prompt.format(
                query=dto.query, courses=[c.model_dump(mode="json") for c in courses]
            )
        )

        ranking_response = CourseRankingLLM.model_validate_json(response.text)

        course_by_id = {c.course_id: c for c in courses}

        ranked_courses = [
            course_by_id[cid]
            for cid in ranking_response.course_ids
            if cid in course_by_id
        ]

        return RecommendationsDTO(
            courses=ranked_courses, skip=dto.skip + len(ranked_courses)
        )
