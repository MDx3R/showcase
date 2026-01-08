from uuid import UUID

from showcase.course.application.dtos.commands.update_skill_command import (
    UpdateSkillCommand,
)
from showcase.course.application.interfaces.repositories.skill_repository import (
    ISkillRepository,
)
from showcase.course.application.interfaces.usecases.command.update_skill_use_case import (
    IUpdateSkillUseCase,
)


class UpdateSkillUseCase(IUpdateSkillUseCase):
    def __init__(self, skill_repository: ISkillRepository) -> None:
        self.skill_repository = skill_repository

    async def execute(self, command: UpdateSkillCommand) -> UUID:
        skill = await self.skill_repository.get_by_id(command.skill_id)

        skill.name = command.name
        skill.description = command.description

        await self.skill_repository.update(skill)
        return command.skill_id
