import logging
import random
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
    RecommendationNotice,
    RecommendationsDTO,
)
from showcase.course.application.read_models.course_read_model import (
    CourseRankingReadModel,
    CourseReadModel,
)
from showcase.course.domain.value_objects.format import Format


class CourseFilterLLM(BaseModel):
    is_decisive: bool = True
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
        logger: logging.Logger,
        llm: LLM,
        course_repository: ICourseReadRepository,
        category_repository: ICategoryReadRepository,
    ) -> None:
        self.llm = llm
        self.course_repository = course_repository
        self.category_repository = category_repository
        self.logger = logger

    async def recommend(self, dto: GetRecommendationsDTO) -> RecommendationsDTO:
        query = dto.query
        self.logger.info(
            "Starting recommendation",
            extra={
                "action": "recommend",
                "input": {"query": dto.query, "limit": dto.limit, "skip": dto.skip},
            },
        )

        # ---------- 1. Categories ----------
        categories = await self.category_repository.get_all()
        category_names = {c.name for c in categories}

        self.logger.info(
            "Categories retrieved",
            extra={
                "action": "get_categories",
                "result": {
                    "count": len(categories),
                    "category_names": list[str](category_names),
                },
            },
        )

        # ---------- 2. LLM → SimpleCoursesFilter ----------
        filter_prompt = PromptTemplate(
            """
            Ты — ассистент подбора образовательных курсов.

            Запрос пользователя:
            "{query}"

            Доступные категории:
            {categories}

            Верни JSON с полями:
            - is_decisive: bool
            - category_names: list[str] | null
            - format: "online" | "offline" | "mixed" | null
            - max_duration_hours: int | null
            - certificate_required: bool | null
            
            Правила для is_decisive:
            Верни true, если запрос осмысленный и составлен на естественном языке,
            даже если он общий или требует уточнений.
            Верни false, если запрос не является осмысленным пользовательским запросом:
            * состоит из случайных символов или чисел
            * содержит только знаки препинания
            * слишком короткий и не несёт смысловой нагрузки

            Если is_decisive = false, верни null для всех остальных полей.

            Если параметр не указан явно — верни null.
            Разрешено использовать только доступные категории, если они есть.
            Если несколько категорий подходят, верни все подходящие в списке category_names.
            Если категорий нет, верни null для category_names.
            Имена категорий чувствительны к регистру.
            """
        )

        filter_llm = self.llm.as_structured_llm(CourseFilterLLM)

        formatted_filter_prompt = filter_prompt.format(
            query=dto.query, categories="\n".join(category_names) or "нет"
        )

        self.logger.info(
            "Sending filter request to LLM",
            extra={
                "action": "llm_filter",
                "input": {
                    "query": dto.query,
                    "categories": ", ".join(category_names) or "нет",
                    "prompt_template": filter_prompt.template,
                },
            },
        )

        response = await filter_llm.acomplete(formatted_filter_prompt)

        filter_response = CourseFilterLLM.model_validate_json(response.text)

        self.logger.info(
            "Filter response received from LLM",
            extra={
                "action": "llm_filter",
                "result": filter_response.model_dump(mode="json"),
            },
        )

        # Indecisive response fallback
        courses = list[CourseReadModel]()
        notices = list[RecommendationNotice]()
        if filter_response.is_decisive and (
            filter_response.category_names
            or filter_response.format
            or filter_response.max_duration_hours
            or filter_response.certificate_required
        ):
            # ---------- 3. Map LLM → SimpleCoursesFilter ----------
            notices.append(RecommendationNotice.FILTERS_INFERRED)
            validated_categories = [
                c for c in filter_response.category_names or [] if c in category_names
            ]
            filter_response.category_names = validated_categories

            filter_query = filter_response.to_filter(
                min(self.MAX_LIMIT, dto.limit), skip=dto.skip
            )

            self.logger.info(
                "Filter mapped to SimpleCoursesFilter",
                extra={
                    "action": "map_filter",
                    "input": filter_response.model_dump(mode="json"),
                    "result": {
                        "categories": filter_query.categories,
                        "format": (
                            filter_query.format.value if filter_query.format else None
                        ),
                        "max_duration_hours": filter_query.max_duration_hours,
                        "certificate_required": filter_query.certificate_required,
                        "limit": filter_query.limit,
                        "skip": filter_query.skip,
                    },
                },
            )

            # ---------- 4. DB filter ----------
            self.logger.info(
                "Filtering courses in database",
                extra={
                    "action": "db_filter",
                    "input": {
                        "categories": filter_query.categories,
                        "format": (
                            filter_query.format.value if filter_query.format else None
                        ),
                        "max_duration_hours": filter_query.max_duration_hours,
                        "certificate_required": filter_query.certificate_required,
                        "limit": filter_query.limit,
                        "skip": filter_query.skip,
                    },
                },
            )

            courses = await self.course_repository.filter(filter_query)

            self.logger.info(
                "Courses filtered from database",
                extra={
                    "action": "db_filter",
                    "result": {
                        "count": len(courses),
                        "course_ids": [str(c.course_id) for c in courses],
                    },
                },
            )

        # ---------- Fallback ----------
        if not courses or not filter_response.is_decisive:
            query = """
            Предложи курсы, отсортированные по предполагаемой востребованности для широкой аудитории.

            Критерии:
            - универсальность
            - актуальность
            - прикладная ценность
            - не нишевость
            """

            notices.extend(
                [
                    (
                        RecommendationNotice.QUERY_INVALID
                        if not filter_response.is_decisive
                        else RecommendationNotice.QUERY_AMBIGUOUS
                    ),
                    RecommendationNotice.FALLBACK_USED,
                ]
            )

            self.logger.info(
                "Courses not found or indecisive",
                extra={
                    "action": "db_filter",
                    "result": {"count": len(courses), "notices": notices},
                },
            )

            courses = await self.course_repository.get_all(limit=self.MAX_LIMIT)

            rng = random.Random()
            rng.shuffle(courses)

            self.logger.info(
                "Courses retrieved and shuffled",
                extra={
                    "action": "db_filter",
                    "result": {
                        "count": len(courses),
                        "notices": notices,
                        "course_ids": [str(c.course_id) for c in courses],
                    },
                },
            )

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

        # Convert to optimized ranking model to reduce token usage
        ranking_courses = [
            CourseRankingReadModel.from_course_read_model(c) for c in courses
        ]
        courses_json = [c.model_dump(mode="json") for c in ranking_courses]

        self.logger.info(
            "Sending ranking request to LLM",
            extra={
                "action": "llm_ranking",
                "input": {
                    "query": query,
                    "courses_count": len(courses),
                    "course_ids": [str(c.course_id) for c in courses],
                    "prompt_template": ranking_prompt.template,
                },
            },
        )

        response = await ranking_llm.acomplete(
            ranking_prompt.format(query=query, courses=courses_json)
        )

        ranking_response = CourseRankingLLM.model_validate_json(response.text)

        self.logger.info(
            "Ranking response received from LLM",
            extra={
                "action": "llm_ranking",
                "result": {
                    "ranked_course_ids": [
                        str(cid) for cid in ranking_response.course_ids
                    ],
                    "count": len(ranking_response.course_ids),
                },
            },
        )

        course_by_id = {c.course_id: c for c in courses}

        ranked_courses = [
            course_by_id[cid]
            for cid in ranking_response.course_ids
            if cid in course_by_id
        ]

        if not ranked_courses:
            self.logger.info(
                "Ranking response is weak",
                extra={"action": "llm_ranking"},
            )

            notices.append(RecommendationNotice.RANKING_WEAK)
            ranked_courses = courses

        result = RecommendationsDTO(
            notices=notices,
            courses=ranked_courses[: min(self.MAX_LIMIT, dto.limit)],
            skip=dto.skip + len(ranked_courses),
        )

        self.logger.info(
            "Recommendation completed",
            extra={
                "action": "recommend",
                "result": {
                    "courses_count": len(ranked_courses),
                    "course_ids": [str(c.course_id) for c in ranked_courses],
                    "skip": result.skip,
                    "notices": notices,
                },
            },
        )

        return result
