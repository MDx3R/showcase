"""Lecturer read repository implementation."""

from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.executor import (
    QueryExecutor,
)
from showcase.lecturer.application.interfaces.repositories import (
    ILecturerReadRepository,
)
from showcase.lecturer.application.read_models.lecturer_read_model import (
    LecturerReadModel,
)
from showcase.lecturer.infrastructure.database.postgres.sqlalchemy.mappers import (
    LecturerReadMapper,
)
from showcase.lecturer.infrastructure.database.postgres.sqlalchemy.models import (
    LecturerBase,
)
from sqlalchemy import select


class LecturerReadRepository(ILecturerReadRepository):
    """Read repository for lecturers."""

    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, lecturer_id: UUID) -> LecturerReadModel:
        """Get a lecturer by ID."""
        stmt = select(LecturerBase).where(LecturerBase.lecturer_id == lecturer_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Lecturer with id {lecturer_id} not found")
        return LecturerReadMapper.to_read_model(model)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[LecturerReadModel]:
        """Get all lecturers."""
        stmt = select(LecturerBase).offset(skip).limit(limit)
        models = await self.executor.execute_scalar_many(stmt)
        return [LecturerReadMapper.to_read_model(model) for model in models]
