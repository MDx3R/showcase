"""Use case interface for deleting a lecturer."""

from abc import ABC, abstractmethod
from uuid import UUID


class IDeleteLecturerUseCase(ABC):
    """Interface for deleting a lecturer."""

    @abstractmethod
    async def execute(self, lecturer_id: UUID) -> UUID:
        """Execute the use case."""
        pass
