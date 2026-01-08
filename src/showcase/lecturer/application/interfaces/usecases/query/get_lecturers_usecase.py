"""Get lecturers use case interface."""

from abc import ABC, abstractmethod

from showcase.lecturer.application.dtos.queries import GetLecturersQuery
from showcase.lecturer.application.read_models.lecturer_read_model import (
    LecturerReadModel,
)


class IGetLecturersUseCase(ABC):
    """Interface for getting lecturers."""

    @abstractmethod
    async def execute(self, query: GetLecturersQuery) -> list[LecturerReadModel]:
        """Execute the get lecturers query."""
        pass
