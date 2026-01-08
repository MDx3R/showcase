"""Use case for getting all skills."""

from showcase.course.application.dtos.queries.get_skills_query import GetSkillsQuery
from showcase.course.application.interfaces.repositories.skill_read_repository import (
    ISkillReadRepository,
)
from showcase.course.application.interfaces.usecases.query.get_skills_use_case import (
    IGetSkillsUseCase,
)
from showcase.course.application.read_models.skill_read_model import SkillReadModel


class GetSkillsUseCase(IGetSkillsUseCase):
    """Implementation of getting all skills."""

    def __init__(self, skill_repository: ISkillReadRepository) -> None:
        self.skill_repository = skill_repository

    async def execute(self, query: GetSkillsQuery) -> list[SkillReadModel]:
        """Execute the use case."""
        return await self.skill_repository.get_all(skip=query.skip, limit=query.limit)
