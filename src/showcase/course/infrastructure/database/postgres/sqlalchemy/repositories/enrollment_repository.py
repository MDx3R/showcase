from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.executor import QueryExecutor
from showcase.course.application.interfaces.repositories.enrollment_repository import (
    IEnrollmentRepository,
)
from showcase.course.domain.entities.enrollment import Enrollment
from showcase.course.infrastructure.database.postgres.sqlalchemy.mappers.enrollment_mapper import (
    EnrollmentMapper,
)
from showcase.course.infrastructure.database.postgres.sqlalchemy.models.enrollment import (
    EnrollmentBase,
)
from sqlalchemy import select


class EnrollmentRepository(IEnrollmentRepository):
    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def add(self, enrollment: Enrollment) -> None:
        persistence = EnrollmentMapper.to_persistence(enrollment)
        await self.executor.add(persistence)

    async def list_by_course(self, course_id: UUID, skip: int = 0, limit: int = 100):
        stmt = (
            select(EnrollmentBase)
            .where(EnrollmentBase.course_id == course_id)
            .offset(skip)
            .limit(limit)
        )
        rows = await self.executor.execute_scalar_many(stmt)
        return [EnrollmentMapper.to_read_model(row) for row in rows]

    async def list_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100):
        stmt = (
            select(EnrollmentBase)
            .where(EnrollmentBase.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        rows = await self.executor.execute_scalar_many(stmt)
        return [EnrollmentMapper.to_read_model(row) for row in rows]
