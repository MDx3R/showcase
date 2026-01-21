"""Read model for filter inference (LLM output)."""

from pydantic import BaseModel
from showcase.course.domain.value_objects.format import Format


class CourseFilterLLM(BaseModel):
    """Structured LLM response for course filter extraction."""

    is_decisive: bool = True
    category_names: list[str] | None = None
    format: Format | None = None
    max_duration_hours: int | None = None
    certificate_required: bool | None = None
