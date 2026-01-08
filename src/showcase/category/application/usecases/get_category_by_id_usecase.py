"""Get category by ID use case implementation."""

from showcase.category.application.dtos.queries import GetCategoryByIdQuery
from showcase.category.application.interfaces.repositories import (
    ICategoryReadRepository,
)
from showcase.category.application.interfaces.usecases.query import (
    IGetCategoryByIdUseCase,
)
from showcase.category.application.read_models.category_read_model import (
    CategoryReadModel,
)


class GetCategoryByIdUseCase(IGetCategoryByIdUseCase):
    """Use case for getting a category by ID."""

    def __init__(self, category_read_repository: ICategoryReadRepository) -> None:
        self.category_read_repository = category_read_repository

    async def execute(self, query: GetCategoryByIdQuery) -> CategoryReadModel:
        """Execute the get category by ID query."""
        return await self.category_read_repository.get_by_id(query.category_id)
