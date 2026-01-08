"""Skill read repository implementation."""

from uuid import UUID

from common.infrastructure.database.postgres.sqlalchemy.executor import QueryExecutor
from showcase.course.application.interfaces.repositories.skill_read_repository import (
    ISkillReadRepository,
)
from showcase.course.application.read_models.skill_read_model import SkillReadModel
from showcase.course.infrastructure.database.postgres.sqlalchemy.mappers.skill_mapper import (
    SkillMapper,
)
from showcase.course.infrastructure.database.postgres.sqlalchemy.models.skill import (
    SkillBase,
)
from sqlalchemy import select


class SkillReadRepository(ISkillReadRepository):
    """Read repository for skills."""

    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[SkillReadModel]:
        """Get all skills."""
        stmt = select(SkillBase).offset(skip).limit(limit)
        models = await self.executor.execute_scalar_many(stmt)
        return [SkillMapper.to_read_model(model) for model in models]

    async def get_by_id(self, skill_id: UUID) -> SkillReadModel:
        """Get a skill by ID."""
        stmt = select(SkillBase).where(SkillBase.skill_id == skill_id)
        model = await self.executor.execute_scalar_one(stmt)
        if not model:
            raise ValueError(f"Skill with id {skill_id} not found")
        return SkillMapper.to_read_model(model)
