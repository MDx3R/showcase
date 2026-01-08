"""Use case interface for updating a tag."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.course.application.dtos.commands.update_tag_command import (
    UpdateTagCommand,
)


class IUpdateTagUseCase(ABC):
    """Interface for updating a tag."""

    @abstractmethod
    async def execute(self, command: UpdateTagCommand) -> UUID:
        """Execute the use case."""
        pass
