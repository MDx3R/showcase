"""Use case interface for deleting a tag."""

from abc import ABC, abstractmethod
from uuid import UUID


class IDeleteTagUseCase(ABC):
    """Interface for deleting a tag."""

    @abstractmethod
    async def execute(self, tag_id: UUID) -> UUID:
        """Execute the use case."""
        pass
