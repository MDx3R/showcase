"""Category write repository implementation."""

from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.executor import QueryExecutor
from showcase.category.application.interfaces.repositories.category_repository import (
    ICategoryRepository,
)
from showcase.category.domain.entities.category import Category
from showcase.category.infrastructure.database.postgres.sqlalchemy.models.category import (
    CategoryBase,
)
from sqlalchemy import delete, select


class CategoryRepository(ICategoryRepository):
    """Write repository for categories."""

    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, category_id: UUID) -> Category:
        """Get a category by ID."""
        stmt = select(CategoryBase).where(CategoryBase.category_id == category_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Category with id {category_id} not found")
        return self._to_domain(model)

    async def add(self, category: Category) -> None:
        """Add a new category."""
        model = self._to_persistence(category)
        await self.executor.add(model)

    async def update(self, category: Category) -> None:
        """Update an existing category."""
        model = self._to_persistence(category)
        await self.executor.save(model)

    async def delete(self, category_id: UUID) -> None:
        """Delete a category by ID."""
        await self.executor.execute(
            delete(CategoryBase).where(CategoryBase.category_id == category_id)
        )

    @staticmethod
    def _to_domain(model: CategoryBase) -> Category:
        """Map ORM model to domain entity."""
        return Category(
            category_id=model.category_id,
            name=model.name,
            description=model.description,
        )

    @staticmethod
    def _to_persistence(entity: Category) -> CategoryBase:
        """Map domain entity to ORM model."""
        return CategoryBase(
            category_id=entity.category_id,
            name=entity.name,
            description=entity.description,
        )
