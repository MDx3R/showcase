"""Use case interface for creating a course."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.course.application.dtos.commands.create_course_command import (
    CreateCourseCommand,
)


class ICreateCourseUseCase(ABC):
    """Interface for creating a course."""

    @abstractmethod
    async def execute(self, command: CreateCourseCommand) -> UUID:
        """Execute the use case."""
        pass
