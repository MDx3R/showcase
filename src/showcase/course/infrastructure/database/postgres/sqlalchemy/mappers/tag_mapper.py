"""Tag read mapper implementation."""

from showcase.course.application.read_models.tag_read_model import TagReadModel
from showcase.course.infrastructure.database.postgres.sqlalchemy.models import TagBase


class TagReadMapper:
    """Maps tag ORM models to read models."""

    @staticmethod
    def to_read_model(model: TagBase) -> TagReadModel:
        """Map tag ORM model to read model."""
        return TagReadModel(tag_id=model.tag_id, name=model.name)


class TagMapper:
    """Alias for backward compatibility."""

    @staticmethod
    def to_read_model(model: TagBase) -> TagReadModel:
        """Map tag ORM model to read model."""
        return TagReadMapper.to_read_model(model)
