"""Lecturer write repository implementation."""

from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.executor import QueryExecutor
from showcase.lecturer.application.interfaces.repositories.lecturer_repository import (
    ILecturerRepository,
)
from showcase.lecturer.domain.entities.lecturer import Lecturer
from showcase.lecturer.infrastructure.database.postgres.sqlalchemy.models.lecturer import (
    LecturerBase,
)
from sqlalchemy import delete, select


class LecturerRepository(ILecturerRepository):
    """Write repository for lecturers."""

    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_by_id(self, lecturer_id: UUID) -> Lecturer:
        """Get a lecturer by ID."""
        stmt = select(LecturerBase).where(LecturerBase.lecturer_id == lecturer_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Lecturer with id {lecturer_id} not found")
        return self._to_domain(model)

    async def add(self, lecturer: Lecturer) -> None:
        """Add a new lecturer."""
        model = self._to_persistence(lecturer)
        await self.executor.add(model)

    async def update(self, lecturer: Lecturer) -> None:
        """Update an existing lecturer."""
        model = self._to_persistence(lecturer)
        await self.executor.save(model)

    async def delete(self, lecturer_id: UUID) -> None:
        """Delete a lecturer by ID."""
        await self.executor.execute(
            delete(LecturerBase).where(LecturerBase.lecturer_id == lecturer_id)
        )

    @staticmethod
    def _to_domain(model: LecturerBase) -> Lecturer:
        """Map ORM model to domain entity."""
        return Lecturer(
            lecturer_id=model.lecturer_id,
            name=model.name,
            position=model.position,
            photo_url=model.photo_url,
            bio=model.bio,
            competencies=model.competencies,
        )

    @staticmethod
    def _to_persistence(entity: Lecturer) -> LecturerBase:
        """Map domain entity to ORM model."""
        return LecturerBase(
            lecturer_id=entity.lecturer_id,
            name=entity.name,
            position=entity.position,
            photo_url=entity.photo_url,
            bio=entity.bio,
            competencies=entity.competencies,
        )
