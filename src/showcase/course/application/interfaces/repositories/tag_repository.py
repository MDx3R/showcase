"""Repository interface for tags write operations."""

from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from uuid import UUID

from showcase.course.domain.entities.tag import Tag


class ITagRepository(ABC):
    """Interface for writing tags."""

    @abstractmethod
    async def get_by_id(self, tag_id: UUID) -> Tag:
        """Get a tag by ID."""
        pass

    @abstractmethod
    async def get_by_values(self, tags: Iterable[str]) -> Sequence[Tag]:
        """Get existing tags by their values."""
        pass

    @abstractmethod
    async def add(self, tag: Tag) -> None:
        """Add a new tag."""
        pass

    @abstractmethod
    async def add_all(self, tags: Iterable[Tag]) -> None:
        """Add new tags."""
        pass

    @abstractmethod
    async def update(self, tag: Tag) -> None:
        """Update an existing tag."""
        pass

    @abstractmethod
    async def delete(self, tag_id: UUID) -> None:
        """Delete a tag by ID."""
        pass
