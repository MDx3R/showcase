from uuid import UUID

from common.domain.interfaces.uuid_generator import IUUIDGenerator
from showcase.course.application.dtos.commands.create_skill_command import (
    CreateSkillCommand,
)
from showcase.course.application.interfaces.repositories.skill_repository import (
    ISkillRepository,
)
from showcase.course.application.interfaces.usecases.command.create_skill_use_case import (
    ICreateSkillUseCase,
)
from showcase.course.domain.entities.skill import Skill


class CreateSkillUseCase(ICreateSkillUseCase):
    def __init__(
        self, uuid_generator: IUUIDGenerator, skill_repository: ISkillRepository
    ) -> None:
        self.uuid_generator = uuid_generator
        self.skill_repository = skill_repository

    async def execute(self, command: CreateSkillCommand) -> UUID:
        skill = Skill(
            skill_id=self.uuid_generator.create(),
            name=command.name,
            description=command.description,
        )
        await self.skill_repository.add(skill)
        return skill.skill_id
