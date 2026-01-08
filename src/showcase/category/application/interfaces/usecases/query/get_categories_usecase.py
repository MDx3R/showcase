"""Get categories use case interface."""

from abc import ABC, abstractmethod

from showcase.category.application.dtos.queries import GetCategoriesQuery
from showcase.category.application.read_models.category_read_model import (
    CategoryReadModel,
)


class IGetCategoriesUseCase(ABC):
    """Interface for getting categories."""

    @abstractmethod
    async def execute(self, query: GetCategoriesQuery) -> list[CategoryReadModel]:
        """Execute the get categories query."""
        pass
