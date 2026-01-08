"""Get lecturer by ID use case interface."""

from abc import ABC, abstractmethod

from showcase.lecturer.application.dtos.queries import GetLecturerByIdQuery
from showcase.lecturer.application.read_models.lecturer_read_model import (
    LecturerReadModel,
)


class IGetLecturerByIdUseCase(ABC):
    """Interface for getting a lecturer by ID."""

    @abstractmethod
    async def execute(self, query: GetLecturerByIdQuery) -> LecturerReadModel:
        """Execute the get lecturer by ID query."""
        pass
