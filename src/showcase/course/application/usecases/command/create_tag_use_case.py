from uuid import UUID

from common.domain.interfaces.uuid_generator import IUUIDGenerator
from showcase.course.application.dtos.commands.create_tag_command import (
    CreateTagCommand,
)
from showcase.course.application.interfaces.repositories.tag_repository import (
    ITagRepository,
)
from showcase.course.application.interfaces.usecases.command.create_tag_use_case import (
    ICreateTagUseCase,
)
from showcase.course.domain.entities.tag import Tag


class CreateTagUseCase(ICreateTagUseCase):
    def __init__(
        self, uuid_generator: IUUIDGenerator, tag_repository: ITagRepository
    ) -> None:
        self.uuid_generator = uuid_generator
        self.tag_repository = tag_repository

    async def execute(self, command: CreateTagCommand) -> UUID:
        tag = Tag(tag_id=self.uuid_generator.create(), value=command.name)
        await self.tag_repository.add(tag)
        return tag.tag_id
