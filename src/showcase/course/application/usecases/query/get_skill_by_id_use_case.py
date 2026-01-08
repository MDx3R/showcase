"""Use case for getting skill by ID."""

from showcase.course.application.dtos.queries.get_skill_by_id_query import (
    GetSkillByIdQuery,
)
from showcase.course.application.interfaces.repositories.skill_read_repository import (
    ISkillReadRepository,
)
from showcase.course.application.interfaces.usecases.query.get_skill_by_id_use_case import (
    IGetSkillByIdUseCase,
)
from showcase.course.application.read_models.skill_read_model import SkillReadModel


class GetSkillByIdUseCase(IGetSkillByIdUseCase):
    """Implementation of getting skill by ID."""

    def __init__(self, skill_repository: ISkillReadRepository) -> None:
        self.skill_repository = skill_repository

    async def execute(self, query: GetSkillByIdQuery) -> SkillReadModel:
        """Execute the use case."""
        return await self.skill_repository.get_by_id(query.skill_id)
