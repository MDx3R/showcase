"""Use case interface for getting all skills."""

from abc import ABC, abstractmethod

from showcase.course.application.dtos.queries.get_skills_query import GetSkillsQuery
from showcase.course.application.read_models.skill_read_model import SkillReadModel


class IGetSkillsUseCase(ABC):
    """Interface for getting all skills."""

    @abstractmethod
    async def execute(self, query: GetSkillsQuery) -> list[SkillReadModel]:
        """Execute the use case."""
        pass
