"""Repository interface for skills read operations."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.course.application.read_models.skill_read_model import SkillReadModel


class ISkillReadRepository(ABC):
    """Interface for reading skills."""

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[SkillReadModel]:
        """Get all skills."""
        pass

    @abstractmethod
    async def get_by_id(self, skill_id: UUID) -> SkillReadModel:
        """Get a skill by ID."""
        pass
