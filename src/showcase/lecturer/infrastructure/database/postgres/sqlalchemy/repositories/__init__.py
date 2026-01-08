"""Lecturer repositories."""

from showcase.lecturer.infrastructure.database.postgres.sqlalchemy.repositories.lecturer_read_repository import (
    LecturerReadRepository,
)
from showcase.lecturer.infrastructure.database.postgres.sqlalchemy.repositories.lecturer_repository import (
    LecturerRepository,
)


__all__ = ["LecturerReadRepository", "LecturerRepository"]
