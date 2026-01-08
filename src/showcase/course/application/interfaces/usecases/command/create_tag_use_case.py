"""Use case interface for creating a tag."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.course.application.dtos.commands.create_tag_command import (
    CreateTagCommand,
)


class ICreateTagUseCase(ABC):
    """Interface for creating a tag."""

    @abstractmethod
    async def execute(self, command: CreateTagCommand) -> UUID:
        """Execute the use case."""
        pass
