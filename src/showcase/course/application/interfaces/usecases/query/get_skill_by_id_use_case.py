"""Use case interface for getting skill by ID."""

from abc import ABC, abstractmethod

from showcase.course.application.dtos.queries.get_skill_by_id_query import (
    GetSkillByIdQuery,
)
from showcase.course.application.read_models.skill_read_model import SkillReadModel


class IGetSkillByIdUseCase(ABC):
    """Interface for getting skill by ID."""

    @abstractmethod
    async def execute(self, query: GetSkillByIdQuery) -> SkillReadModel:
        """Execute the use case."""
        pass
