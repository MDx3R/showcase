"""Category read repository implementation."""

from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.executor import (
    QueryExecutor,
)
from showcase.category.application.interfaces.repositories import (
    ICategoryReadRepository,
)
from showcase.category.application.read_models.category_read_model import (
    CategoryReadModel,
)
from showcase.category.infrastructure.database.postgres.sqlalchemy.mappers import (
    CategoryReadMapper,
)
from showcase.category.infrastructure.database.postgres.sqlalchemy.models import (
    CategoryBase,
)
from sqlalchemy import select


class CategoryReadRepository(ICategoryReadRepository):
    """Read repository for categories."""

    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, category_id: UUID) -> CategoryReadModel:
        """Get a category by ID."""
        stmt = select(CategoryBase).where(CategoryBase.category_id == category_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Category with id {category_id} not found")
        return CategoryReadMapper.to_read_model(model)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[CategoryReadModel]:
        """Get all categories with optional filters."""
        stmt = select(CategoryBase).offset(skip).limit(limit)

        models = await self.executor.execute_scalar_many(stmt)
        return [CategoryReadMapper.to_read_model(model) for model in models]
