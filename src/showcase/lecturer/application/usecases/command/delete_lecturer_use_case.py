from uuid import UUID

from showcase.lecturer.application.interfaces.repositories.lecturer_repository import (
    ILecturerRepository,
)
from showcase.lecturer.application.interfaces.usecases.command.delete_lecturer_use_case import (
    IDeleteLecturerUseCase,
)


class DeleteLecturerUseCase(IDeleteLecturerUseCase):
    def __init__(self, lecturer_repository: ILecturerRepository) -> None:
        self.lecturer_repository = lecturer_repository

    async def execute(self, lecturer_id: UUID) -> UUID:
        await self.lecturer_repository.delete(lecturer_id)
        return lecturer_id
