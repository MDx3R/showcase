from uuid import UUID

from showcase.category.application.interfaces.repositories.category_repository import (
    ICategoryRepository,
)
from showcase.category.application.interfaces.usecases.command.delete_category_use_case import (
    IDeleteCategoryUseCase,
)


class DeleteCategoryUseCase(IDeleteCategoryUseCase):
    def __init__(self, category_repository: ICategoryRepository) -> None:
        self.category_repository = category_repository

    async def execute(self, category_id: UUID) -> UUID:
        await self.category_repository.delete(category_id)
        return category_id
