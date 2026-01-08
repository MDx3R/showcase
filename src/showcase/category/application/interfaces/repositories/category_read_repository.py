"""Category read repository interface."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.category.application.read_models.category_read_model import (
    CategoryReadModel,
)


class ICategoryReadRepository(ABC):
    """Interface for reading categories."""

    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> CategoryReadModel:
        """Get a category by ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[CategoryReadModel]:
        """Get all categories with optional filters."""
        pass
