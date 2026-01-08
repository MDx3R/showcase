"""Category read mapper implementation."""

from showcase.category.application.read_models.category_read_model import (
    CategoryReadModel,
)
from showcase.category.infrastructure.database.postgres.sqlalchemy.models import (
    CategoryBase,
)


class CategoryReadMapper:
    """Maps ORM models to read models."""

    @staticmethod
    def to_read_model(model: CategoryBase) -> CategoryReadModel:
        """Map ORM model to read model."""
        return CategoryReadModel(
            category_id=model.category_id,
            name=model.name,
            description=model.description,
        )
