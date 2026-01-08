"""Use case interface for updating a course."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.course.application.dtos.commands.update_course_command import (
    UpdateCourseCommand,
)


class IUpdateCourseUseCase(ABC):
    """Interface for updating a course."""

    @abstractmethod
    async def execute(self, command: UpdateCourseCommand) -> UUID:
        """Execute the use case."""
        pass
