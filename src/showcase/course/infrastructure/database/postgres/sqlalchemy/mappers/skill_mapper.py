"""Skill read mapper within course bounded context."""

from showcase.course.application.read_models.skill_read_model import SkillReadModel
from showcase.course.infrastructure.database.postgres.sqlalchemy.models import SkillBase


class SkillReadMapper:
    """Maps ORM models to read models."""

    @staticmethod
    def to_read_model(model: SkillBase) -> SkillReadModel:
        """Map ORM model to read model."""
        return SkillReadModel(
            skill_id=model.skill_id, name=model.name, description=model.description
        )


class SkillMapper:
    """Alias for backward compatibility."""

    @staticmethod
    def to_read_model(model: SkillBase) -> SkillReadModel:
        """Map ORM model to read model."""
        return SkillReadMapper.to_read_model(model)
