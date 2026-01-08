"""Use case interface for creating a lecturer."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.lecturer.application.dtos.commands.create_lecturer_command import (
    CreateLecturerCommand,
)


class ICreateLecturerUseCase(ABC):
    """Interface for creating a lecturer."""

    @abstractmethod
    async def execute(self, command: CreateLecturerCommand) -> UUID:
        """Execute the use case."""
        pass
