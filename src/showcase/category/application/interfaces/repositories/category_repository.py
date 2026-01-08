"""Repository interface for category write operations."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.category.domain.entities.category import Category


class ICategoryRepository(ABC):
    """Interface for writing categories."""

    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> Category:
        """Get a category by ID."""
        pass

    @abstractmethod
    async def add(self, category: Category) -> None:
        """Add a new category."""
        pass

    @abstractmethod
    async def update(self, category: Category) -> None:
        """Update an existing category."""
        pass

    @abstractmethod
    async def delete(self, category_id: UUID) -> None:
        """Delete a category by ID."""
        pass
