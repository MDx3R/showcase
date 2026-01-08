"""Category use case implementations."""

from showcase.category.application.dtos.queries import GetCategoriesQuery
from showcase.category.application.interfaces.repositories import (
    ICategoryReadRepository,
)
from showcase.category.application.interfaces.usecases.query import (
    IGetCategoriesUseCase,
)
from showcase.category.application.read_models.category_read_model import (
    CategoryReadModel,
)


class GetCategoriesUseCase(IGetCategoriesUseCase):
    """Use case for getting categories."""

    def __init__(self, category_read_repository: ICategoryReadRepository) -> None:
        self.category_read_repository = category_read_repository

    async def execute(self, query: GetCategoriesQuery) -> list[CategoryReadModel]:
        """Execute the get categories query."""
        return await self.category_read_repository.get_all(
            skip=query.skip, limit=query.limit
        )
