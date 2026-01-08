"""Get lecturer by ID use case implementation."""

from showcase.lecturer.application.dtos.queries import GetLecturerByIdQuery
from showcase.lecturer.application.interfaces.repositories import (
    ILecturerReadRepository,
)
from showcase.lecturer.application.interfaces.usecases.query import (
    IGetLecturerByIdUseCase,
)
from showcase.lecturer.application.read_models.lecturer_read_model import (
    LecturerReadModel,
)


class GetLecturerByIdUseCase(IGetLecturerByIdUseCase):
    """Use case for getting a lecturer by ID."""

    def __init__(self, lecturer_read_repository: ILecturerReadRepository) -> None:
        self.lecturer_read_repository = lecturer_read_repository

    async def execute(self, query: GetLecturerByIdQuery) -> LecturerReadModel:
        """Execute the get lecturer by ID query."""
        return await self.lecturer_read_repository.get_by_id(query.lecturer_id)
