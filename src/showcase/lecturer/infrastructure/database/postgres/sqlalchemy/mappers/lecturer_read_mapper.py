"""Lecturer read mapper implementation."""

from showcase.lecturer.application.read_models.lecturer_read_model import (
    LecturerReadModel,
)
from showcase.lecturer.infrastructure.database.postgres.sqlalchemy.models import (
    LecturerBase,
)


class LecturerReadMapper:
    """Maps ORM models to read models."""

    @staticmethod
    def to_read_model(model: LecturerBase) -> LecturerReadModel:
        """Map ORM model to read model."""
        return LecturerReadModel(
            lecturer_id=model.lecturer_id,
            name=model.name,
            position=model.position,
            bio=model.bio,
            photo_url=model.photo_url,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
