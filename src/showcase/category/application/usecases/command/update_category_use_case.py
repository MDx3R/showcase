from uuid import UUID

from showcase.category.application.dtos.commands.update_category_command import (
    UpdateCategoryCommand,
)
from showcase.category.application.interfaces.repositories.category_repository import (
    ICategoryRepository,
)
from showcase.category.application.interfaces.usecases.command.update_category_use_case import (
    IUpdateCategoryUseCase,
)


class UpdateCategoryUseCase(IUpdateCategoryUseCase):
    def __init__(self, category_repository: ICategoryRepository) -> None:
        self.category_repository = category_repository

    async def execute(self, command: UpdateCategoryCommand) -> UUID:
        category = await self.category_repository.get_by_id(command.category_id)
        if command.name is not None:
            category.name = command.name
        if command.description is not None:
            category.description = command.description
        await self.category_repository.update(category)
        return command.category_id
