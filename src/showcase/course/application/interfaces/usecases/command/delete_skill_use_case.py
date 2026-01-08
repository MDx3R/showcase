"""Use case interface for deleting a skill."""

from abc import ABC, abstractmethod
from uuid import UUID


class IDeleteSkillUseCase(ABC):
    """Interface for deleting a skill."""

    @abstractmethod
    async def execute(self, skill_id: UUID) -> UUID:
        """Execute the use case."""
        pass
