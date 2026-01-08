from uuid import UUID

from showcase.lecturer.application.dtos.commands.update_lecturer_command import (
    UpdateLecturerCommand,
)
from showcase.lecturer.application.interfaces.repositories.lecturer_repository import (
    ILecturerRepository,
)
from showcase.lecturer.application.interfaces.usecases.command.update_lecturer_use_case import (
    IUpdateLecturerUseCase,
)


class UpdateLecturerUseCase(IUpdateLecturerUseCase):
    def __init__(self, lecturer_repository: ILecturerRepository) -> None:
        self.lecturer_repository = lecturer_repository

    async def execute(self, command: UpdateLecturerCommand) -> UUID:
        lecturer = await self.lecturer_repository.get_by_id(command.lecturer_id)

        lecturer.name = command.name
        lecturer.position = command.position
        lecturer.bio = command.bio
        lecturer.photo_url = command.photo_url
        lecturer.competencies = command.competencies

        await self.lecturer_repository.update(lecturer)
        return command.lecturer_id
