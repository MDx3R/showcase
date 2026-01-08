"""Repository interface for skills write operations."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.course.domain.entities.skill import Skill


class ISkillRepository(ABC):
    """Interface for writing skills."""

    @abstractmethod
    async def get_by_id(self, skill_id: UUID) -> Skill:
        """Get a skill by ID."""
        pass

    @abstractmethod
    async def add(self, skill: Skill) -> None:
        """Add a new skill."""
        pass

    @abstractmethod
    async def update(self, skill: Skill) -> None:
        """Update an existing skill."""
        pass

    @abstractmethod
    async def delete(self, skill_id: UUID) -> None:
        """Delete a skill by ID."""
        pass
