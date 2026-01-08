from uuid import UUID

from common.domain.interfaces.uuid_generator import IUUIDGenerator
from showcase.category.application.dtos.commands.create_category_command import (
    CreateCategoryCommand,
)
from showcase.category.application.interfaces.repositories.category_repository import (
    ICategoryRepository,
)
from showcase.category.application.interfaces.usecases.command.create_category_use_case import (
    ICreateCategoryUseCase,
)
from showcase.category.domain.entities.category import Category


class CreateCategoryUseCase(ICreateCategoryUseCase):
    def __init__(
        self, uuid_generator: IUUIDGenerator, category_repository: ICategoryRepository
    ) -> None:
        self.uuid_generator = uuid_generator
        self.category_repository = category_repository

    async def execute(self, command: CreateCategoryCommand) -> UUID:
        category = Category(
            category_id=self.uuid_generator.create(),
            name=command.name,
            description=command.description,
        )
        await self.category_repository.add(category)
        return category.category_id
