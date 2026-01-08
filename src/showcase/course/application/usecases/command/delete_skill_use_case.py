from uuid import UUID

from showcase.course.application.interfaces.repositories.skill_repository import (
    ISkillRepository,
)
from showcase.course.application.interfaces.usecases.command.delete_skill_use_case import (
    IDeleteSkillUseCase,
)


class DeleteSkillUseCase(IDeleteSkillUseCase):
    def __init__(self, skill_repository: ISkillRepository) -> None:
        self.skill_repository = skill_repository

    async def execute(self, skill_id: UUID) -> UUID:
        await self.skill_repository.delete(skill_id)
        return skill_id
