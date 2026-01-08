"""Use case interface for deleting a category."""

from abc import ABC, abstractmethod
from uuid import UUID


class IDeleteCategoryUseCase(ABC):
    """Interface for deleting a category."""

    @abstractmethod
    async def execute(self, category_id: UUID) -> UUID:
        """Execute the use case."""
        pass
