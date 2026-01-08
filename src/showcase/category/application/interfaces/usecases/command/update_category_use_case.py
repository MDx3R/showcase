"""Use case interface for updating a category."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.category.application.dtos.commands.update_category_command import (
    UpdateCategoryCommand,
)


class IUpdateCategoryUseCase(ABC):
    """Interface for updating a category."""

    @abstractmethod
    async def execute(self, command: UpdateCategoryCommand) -> UUID:
        """Execute the use case."""
        pass
