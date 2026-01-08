"""Use case interface for creating a skill."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.course.application.dtos.commands.create_skill_command import (
    CreateSkillCommand,
)


class ICreateSkillUseCase(ABC):
    """Interface for creating a skill."""

    @abstractmethod
    async def execute(self, command: CreateSkillCommand) -> UUID:
        """Execute the use case."""
        pass
