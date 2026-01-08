from uuid import UUID

from showcase.course.application.dtos.commands.update_tag_command import (
    UpdateTagCommand,
)
from showcase.course.application.interfaces.repositories.tag_repository import (
    ITagRepository,
)
from showcase.course.application.interfaces.usecases.command.update_tag_use_case import (
    IUpdateTagUseCase,
)


class UpdateTagUseCase(IUpdateTagUseCase):
    def __init__(self, tag_repository: ITagRepository) -> None:
        self.tag_repository = tag_repository

    async def execute(self, command: UpdateTagCommand) -> UUID:
        tag = await self.tag_repository.get_by_id(command.tag_id)

        tag.value = command.name
        await self.tag_repository.update(tag)

        return command.tag_id
