"""Lecturer use case implementations."""

from showcase.lecturer.application.dtos.queries import GetLecturersQuery
from showcase.lecturer.application.interfaces.repositories import (
    ILecturerReadRepository,
)
from showcase.lecturer.application.interfaces.usecases.query import (
    IGetLecturersUseCase,
)
from showcase.lecturer.application.read_models.lecturer_read_model import (
    LecturerReadModel,
)


class GetLecturersUseCase(IGetLecturersUseCase):
    """Use case for getting lecturers."""

    def __init__(self, lecturer_read_repository: ILecturerReadRepository) -> None:
        self.lecturer_read_repository = lecturer_read_repository

    async def execute(self, query: GetLecturersQuery) -> list[LecturerReadModel]:
        """Execute the get lecturers query."""
        return await self.lecturer_read_repository.get_all(
            skip=query.skip, limit=query.limit
        )
