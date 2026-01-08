from uuid import UUID

from common.domain.interfaces.uuid_generator import IUUIDGenerator
from showcase.lecturer.application.dtos.commands.create_lecturer_command import (
    CreateLecturerCommand,
)
from showcase.lecturer.application.interfaces.repositories.lecturer_repository import (
    ILecturerRepository,
)
from showcase.lecturer.application.interfaces.usecases.command.create_lecturer_use_case import (
    ICreateLecturerUseCase,
)
from showcase.lecturer.domain.entities.lecturer import Lecturer


class CreateLecturerUseCase(ICreateLecturerUseCase):
    def __init__(
        self, uuid_generator: IUUIDGenerator, lecturer_repository: ILecturerRepository
    ) -> None:
        self.uuid_generator = uuid_generator
        self.lecturer_repository = lecturer_repository

    async def execute(self, command: CreateLecturerCommand) -> UUID:
        lecturer = Lecturer(
            lecturer_id=self.uuid_generator.create(),
            name=command.name,
            position=command.position,
            bio=command.bio,
            photo_url=command.photo_url,
        )
        await self.lecturer_repository.add(lecturer)
        return lecturer.lecturer_id
