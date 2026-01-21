"""Filter inference: LLM-based extraction of course filter from user query."""

import logging

from llama_index.core import PromptTemplate
from llama_index.core.llms import LLM
from pydantic import BaseModel

from showcase.course.domain.value_objects.format import Format


class CourseFilterLLM(BaseModel):
    """Structured LLM response for course filter extraction."""

    is_decisive: bool = True
    category_names: list[str] | None = None
    format: Format | None = None
    max_duration_hours: int | None = None
    certificate_required: bool | None = None


FILTER_PROMPT = PromptTemplate(
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


class FilterInferenceService:
    """Infers structured course filter from user query using LLM."""

    def __init__(self, logger: logging.Logger, llm: LLM) -> None:
        self._logger = logger
        self._llm = llm

    async def infer(self, query: str, category_names: set[str]) -> CourseFilterLLM:
        """Infers CourseFilterLLM from user query and available categories."""
        categories_str = "\n".join(sorted(category_names)) if category_names else "нет"

        self._logger.debug(
            "Inferring filter from query",
            extra={
                "service": "FilterInference",
                "query": query[:200],
                "categories_count": len(category_names),
            },
        )

        filter_llm = self._llm.as_structured_llm(CourseFilterLLM)
        formatted = FILTER_PROMPT.format(query=query, categories=categories_str)
        response = await filter_llm.acomplete(formatted)
        result = CourseFilterLLM.model_validate_json(response.text)

        self._logger.info(
            "Filter inferred",
            extra={
                "service": "FilterInference",
                "is_decisive": result.is_decisive,
                "has_category_names": bool(result.category_names),
                "format": result.format.value if result.format else None,
                "max_duration_hours": result.max_duration_hours,
                "certificate_required": result.certificate_required,
            },
        )

        return result
