"""Repository interface for tags read operations."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.course.application.read_models.tag_read_model import TagReadModel


class ITagReadRepository(ABC):
    """Interface for reading tags."""

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[TagReadModel]:
        """Get all tags."""
        pass

    @abstractmethod
    async def get_by_id(self, tag_id: UUID) -> TagReadModel:
        """Get a tag by ID."""
        pass
