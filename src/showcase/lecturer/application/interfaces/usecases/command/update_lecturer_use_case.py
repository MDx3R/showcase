"""Use case interface for updating a lecturer."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.lecturer.application.dtos.commands.update_lecturer_command import (
    UpdateLecturerCommand,
)


class IUpdateLecturerUseCase(ABC):
    """Interface for updating a lecturer."""

    @abstractmethod
    async def execute(self, command: UpdateLecturerCommand) -> UUID:
        """Execute the use case."""
        pass
