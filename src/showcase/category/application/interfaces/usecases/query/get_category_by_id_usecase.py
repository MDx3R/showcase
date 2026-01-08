"""Get category by ID use case interface."""

from abc import ABC, abstractmethod

from showcase.category.application.dtos.queries import GetCategoryByIdQuery
from showcase.category.application.read_models.category_read_model import (
    CategoryReadModel,
)


class IGetCategoryByIdUseCase(ABC):
    """Interface for getting a category by ID."""

    @abstractmethod
    async def execute(self, query: GetCategoryByIdQuery) -> CategoryReadModel:
        """Execute the get category by ID query."""
        pass
