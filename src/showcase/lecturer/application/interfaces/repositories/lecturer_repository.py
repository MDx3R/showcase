"""Repository interface for lecturer write operations."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.lecturer.domain.entities.lecturer import Lecturer


class ILecturerRepository(ABC):
    """Interface for writing lecturers."""

    @abstractmethod
    async def get_by_id(self, lecturer_id: UUID) -> Lecturer:
        """Get a lecturer by ID."""
        pass

    @abstractmethod
    async def add(self, lecturer: Lecturer) -> None:
        """Add a new lecturer."""
        pass

    @abstractmethod
    async def update(self, lecturer: Lecturer) -> None:
        """Update an existing lecturer."""
        pass

    @abstractmethod
    async def delete(self, lecturer_id: UUID) -> None:
        """Delete a lecturer by ID."""
        pass
