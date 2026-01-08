"""Use case interface for updating a skill."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.course.application.dtos.commands.update_skill_command import (
    UpdateSkillCommand,
)


class IUpdateSkillUseCase(ABC):
    """Interface for updating a skill."""

    @abstractmethod
    async def execute(self, command: UpdateSkillCommand) -> UUID:
        """Execute the use case."""
        pass
