"""Lecturer read repository interface."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.lecturer.application.read_models.lecturer_read_model import (
    LecturerReadModel,
)


class ILecturerReadRepository(ABC):
    """Interface for reading lecturers."""

    @abstractmethod
    async def get_by_id(self, lecturer_id: UUID) -> LecturerReadModel:
        """Get a lecturer by ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[LecturerReadModel]:
        """Get all lecturers."""
        pass
