"""Use case interface for creating a category."""

from abc import ABC, abstractmethod
from uuid import UUID

from showcase.category.application.dtos.commands.create_category_command import (
    CreateCategoryCommand,
)


class ICreateCategoryUseCase(ABC):
    """Interface for creating a category."""

    @abstractmethod
    async def execute(self, command: CreateCategoryCommand) -> UUID:
        """Execute the use case."""
        pass
